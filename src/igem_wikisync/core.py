import os
import shutil
from hashlib import md5
from http.cookiejar import LWPCookieJar
from pathlib import Path

import mechanicalsoup
import yaml

from igem_wikisync.browser import iGEM_login
from igem_wikisync.browser import iGEM_upload_file
from igem_wikisync.browser import iGEM_upload_page
from igem_wikisync.code import CSSparser
from igem_wikisync.code import HTMLparser
from igem_wikisync.code import JSparser
from igem_wikisync.files import CSSfile
from igem_wikisync.files import HTMLfile
from igem_wikisync.files import JSfile
from igem_wikisync.files import OtherFile
from igem_wikisync.logger import logger


def wikisync(team, src_dir, build_dir, assets,  config=None):

    if team is None:
        logger.critical("Please specify your team name.")
        raise SystemExit

    if src_dir is None:
        logger.critical('Please specify where we should look for your code using the src_dir argument.')
        raise SystemExit

    if build_dir is None:
        logger.critical('Please specify where we should build your code using the build_dir argument.')
        raise SystemExit

    if assets is None:
        logger.critical('Please specify where your assets are using the assets argument.')
        raise SystemExit

    if type(assets) != list:
        logger.critical('The assets argument should point to a list of directories.')
        raise SystemExit

    if config is None:
        config = {
            'team':      team,
            'src_dir':   src_dir,
            'build_dir': build_dir
        }
    else:
        # read config file
        try:
            with open(config, 'r') as file:
                config = yaml.safe_load(file)
        except Exception:
            logger.critical(f"No {config} file found. Exiting.")
            raise SystemExit


    # load or create upload_map
    try:
        with open('upload_map.yml', 'r') as file:
            upload_map = yaml.safe_load(file)

        # make sure upload map has all the keys
        for key in ['assets', 'html', 'css', 'js']:
            if key not in upload_map.keys():
                upload_map[key] = {}
            elif type(upload_map[key]) != dict:
                logger.critical("config.yml has an invalid format. Exiting.")
                raise SystemExit
    except BaseException:
        upload_map = {
            'assets': {},
            'html': {},
            'css': {},
            'js': {}
        }

    # clear build_dir
    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir)
        os.mkdir(build_dir)
        # ? error handling here?

    # get iGEM credentials
    credentials = {
        'username': os.environ.get('IGEM_USERNAME'),
        'password': os.environ.get('IGEM_PASSWORD'),
        'team': team
    }

    # declare a global browser instance
    browser = mechanicalsoup.StatefulBrowser()
    # ? error handling here?

    # Load cookies from file or create new cookie file
    cookie_file = 'igemwiki-upload.cookies'
    cookiejar = LWPCookieJar(cookie_file)
    if os.path.exists(cookie_file):
        try:
            cookiejar.load()  # in case file is empty
        except Exception:
            pass
    browser.set_cookiejar(cookiejar)

    # login to iGEM
    login = iGEM_login(browser, credentials)
    if not login:
        message = "Failed to login."
        logger.error(message)
        raise SystemExit

    # Save cookies
    cookiejar.save()

    # storage
    HTMLfiles = {}
    CSSfiles = {}
    JSfiles = {}
    OtherFiles = {}

    # for each file in src_dir
    for root, _, files in os.walk(src_dir):
        for filename in files:

            infile = Path(root) / Path(filename)
            extension = infile.suffix[1:].lower()

            # create appropriate file object
            # file objects contain corresponding paths and URLs
            if extension == "html":

                file_object = HTMLfile(infile, config)

                # and store it
                HTMLfiles[file_object.path] = file_object

                # and add it to the upload map
                if file_object.path not in upload_map['html'].keys():
                    upload_map['html'][str(file_object.path)] = {
                        'md5': '',
                        'link_URL': file_object.link_URL
                    }

            elif extension == "css":

                file_object = CSSfile(infile, config)

                CSSfiles[file_object.path] = file_object

                if file_object.path not in upload_map['css'].keys():
                    upload_map['css'][str(file_object.path)] = {
                        'md5': '',
                        'link_URL': file_object.link_URL
                    }

            elif extension == "js":

                file_object = JSfile(infile, config)

                JSfiles[file_object.path] = file_object

                if file_object.path not in upload_map['js'].keys():
                    upload_map['js'][str(file_object.path)] = {
                        'md5': '',
                        'link_URL': file_object.link_URL
                    }

            elif extension.lower() in ['png', 'gif', 'jpg', 'jpeg', 'pdf', 'ppt', 'txt',
                                       'zip', 'mp3', 'mp4', 'webm', 'mov', 'swf', 'xls',
                                       'xlsx', 'docx', 'pptx', 'csv', 'm', 'ogg', 'gb',
                                       'tif', 'tiff', 'fcs', 'otf', 'eot', 'ttf', 'woff', 'svg']:

                file_object = OtherFile(infile, config)

                OtherFiles[file_object.path] = file_object

            else:
                logger.info(f"{infile} has an unsupported file extension. Skipping.")
                # ? Do we want to support other text files?

    # *Upload all assets and create a map
    # files have to be uploaded before everything else because
    # the URLs iGEM assigns are random
    for path in OtherFiles.keys():
        file_object = OtherFiles[path]
        uploaded = False  # flag to keep track of current file upload

        # check if the file has already been uploaded
        for asset_path in upload_map['assets'].keys():

            if asset_path == str(path):
                asset = upload_map['assets'][asset_path]
                if file_object.md5_hash == asset['md5']:
                    # ? Can't do anything about renames. iGEM API doesn't allow.
                    # ? Can find the previous URL and use that itself
                    # ? but is it worth the effort?
                    pass
                else:
                    # if file has changed, upload file and update hash
                    try:
                        iGEM_upload_file(browser, file_object)
                    except BaseException:
                        # print upload map to save the current state
                        write_upload_map(upload_map)
                        message = f"Failed to upload {str(file_object.path)}. " + \
                            "The current upload map has been saved so you won't have to upload everything again."
                        logger.debug(message, exc_info=True)
                        logger.error(message)
                        raise SystemExit

                    # TODO: add error handling
                    asset['md5'] = file_object.md5_hash
                    asset['link_URL'] = file_object.upload_URL

                uploaded = True
                break

        # if new file, upload and add to map
        if not uploaded:
            try:
                iGEM_upload_file(browser, file_object)
            except BaseException:
                # print upload map to save the current state
                write_upload_map(upload_map)
                message = f"Failed to upload {str(file_object.path)}. " + \
                    "The current upload map has been saved so you won't have to upload everything again."
                logger.debug(message, exc_info=True)
                logger.error(message)
                raise SystemExit

            upload_map['assets'][str(path)] = {
                'link_URL': file_object.upload_URL,
                'md5': file_object.md5_hash,
                'upload_filename': file_object.upload_filename
            }

    # write upload map just in case
    # things go wrong while dealing with code
    write_upload_map(upload_map)

    # loop through all code files
    for file_dictionary in [HTMLfiles, CSSfiles, JSfiles]:
        for path in file_dictionary.keys():
            file_object = file_dictionary[path]
            path_str = str(file_object.path)
            ext = file_object.extension

            # open file
            try:
                with open(file_object.src_path, 'r') as file:
                    contents = file.read()
            except Exception:
                message = f"Couldn't open/read {file_object.path}. Skipping."
                logger.error(message)
                continue
                # FIXME Can this be improved?

            processed = None  # just so the linter doesn't freak out
            # parse and modify contents
            if ext == 'html':
                processed = HTMLparser(
                    config, file_object.path, contents, upload_map)
                # FIXME error handling here?
            elif ext == 'css':
                processed = CSSparser(
                    config, file_object.path, contents, upload_map)
                # FIXME error handling here?
            elif ext == 'js':
                processed = JSparser(contents)
                # FIXME error handling here?

            # calculate and store md5 hash of the modified contents
            build_hash = md5(processed.encode('utf-8')).hexdigest()

            if upload_map[ext][path_str]['md5'] == build_hash:
                message = f"Contents of {file_object.path} have been uploaded previously. Skipping."
                logger.info(message)
            else:
                upload_map[ext][path_str]['md5'] = build_hash
                build_path = file_object.build_path
                try:
                    # create directory if doesn't exist
                    if not os.path.isdir(build_path.parent):
                        os.makedirs(build_path.parent)
                    # and write the processed contents
                    with open(build_path, 'w') as f:
                        f.write(processed)
                except Exception:
                    message = f"Couldn't write {build_dir}/{str(file_object.path)}. Skipping."
                    logger.info(message)
                    continue
                    # FIXME Can this be improved?

                # upload
                try:
                    iGEM_upload_page(browser, processed,
                                     file_object.upload_URL)
                except BaseException:
                    message = f"Couldn't upload {str(file_object.path)}. Skipping."
                    logger.info(message)
                    continue
                    # FIXME Can this be improved?

    # write final upload map
    write_upload_map(upload_map)


def write_upload_map(upload_map, filename='upload_map.yml'):
    try:
        with open(filename, 'w') as file:
            yaml.dump(upload_map, file, sort_keys=True)
    except Exception:
        logger.error(f"Tried to write {filename} but couldn't.")
        # FIXME Can this be improved?
