import os
from hashlib import md5
from http.cookiejar import LWPCookieJar
from pathlib import Path

import mechanicalsoup
import yaml

from igem_wikisync.browser import iGEM_login, iGEM_upload_file, iGEM_upload_page
from igem_wikisync.parsers import HTMLparser, CSSparser, JSparser
from igem_wikisync.files import HTMLfile, CSSfile, JSfile, OtherFile
from igem_wikisync.logger import logger

# pylint: disable=too-many-instance-attributes, fixme


def run(team: str, src_dir: str, build_dir: str):
    '''
    Runs iGEM-WikiSync and uploads all files to iGEM servers
    while replacing relative URLs with those on the iGEM server.

    Arguments:
        # @param team: iGEM Team Name
        src_dir: Path to the folder where the source files are present
        build_dir: Path to the folder where the built files will be stored before uploading
    '''

    # TODO: does it store files in build_dir also?

    # * 1. CHECK AND FORMAT INPUTS
    if team is None or not isinstance(team, str):
        logger.critical('Please specify your team name.')
        raise SystemExit

    if src_dir is None or not isinstance(src_dir, str):
        logger.critical('Please specify where we should look for your code ' +
                        'using the src_dir argument.')
        raise SystemExit

    if build_dir is None or not isinstance(build_dir, str):
        logger.critical('Please specify where we should build your code ' +
                        'using the build_dir argument.')
        raise SystemExit

    config = {
        'team':      team,
        'src_dir':   src_dir,
        'build_dir': build_dir
    }

    # * 2. Load or create upload_map
    upload_map = get_upload_map()

    # * 3. Create build directory
    if not os.path.isdir(build_dir):
        os.mkdir(build_dir)
        # ? error handling here?

    # * 4. Get iGEM credentials from environment variables
    credentials = {
        'username': os.environ.get('IGEM_USERNAME'),
        'password': os.environ.get('IGEM_PASSWORD'),
        'team': team
    }

    # * 5. Load/create cookie file
    browser, cookiejar = get_browser_with_cookies()

    # * 6. Login to iGEM
    login = iGEM_login(browser, credentials)
    if not login:
        message = 'Failed to login.'
        logger.error(message)
        raise SystemExit

    # * 7. Save cookies
    # TODO: check if this works, might not
    cookiejar.save()

    # * 8. Cache files
    files = cache_files(upload_map, config)

    # * 9. Upload all assets and create a map
    upload_assets(files['other'], browser, upload_map)

    # * 10. write upload map just in case
    # things go wrong while dealing with code
    write_upload_map(upload_map)

    # * 11. Build files and upload changed files
    build_and_upload(files, browser, config, upload_map)

    # * 12. Write final upload map
    write_upload_map(upload_map)


def get_upload_map():
    """
    Opens existing upload_map.yml or creates and empty upload map.

    Upload map is a dictionary that contains previously uploaded
    html, css, js and other files, along with their URLs and hashes.
    """

    if os.path.isfile('upload_map.yml'):
        try:
            with open('upload_map.yml', 'r') as file:
                upload_map = yaml.safe_load(file)
        except Exception:
            logger.critical('upload_map.yml exists but could not be opened.')
            logger.critical('Please fix/delete the file and run the program again.')
            raise SystemExit

        if isinstance(upload_map, type(None)):
            upload_map = {}

        # make sure upload map has all the keys
        for key in ['assets', 'html', 'css', 'js']:
            if key not in upload_map.keys() or isinstance(upload_map[key], type(None)):
                upload_map[key] = {}
            elif not isinstance(upload_map[key], dict):
                logger.critical('upload_map.yml has an invalid format.')
                logger.critical('Please fix/delete the file and run the program again.')
                raise SystemExit

        return upload_map
    else:
        return {
            'assets': {},
            'html': {},
            'css': {},
            'js': {}
        }


def write_upload_map(upload_map: dict, filename='upload_map.yml'):
    """ Writes upload map to file. """

    try:
        with open(filename, 'w') as file:
            yaml.dump(upload_map, file, sort_keys=True)
    except Exception:
        logger.error(f'Tried to write {filename} but could not.')
        # FIXME Can this be improved?
        return False

    return True


def get_browser_with_cookies():
    """
    Creates a mechanicalsoup.StatefulBrowser() instance
    with cookies loaded from file, if exists.

    Returns:
        browser: mechanicalsoup.StatefulBrowser() instance
        cookiejar: browser cookiejar that can be saved after logging in
    """

    cookie_file = 'igemwiki-upload.cookies'
    cookiejar = LWPCookieJar(cookie_file)
    if os.path.exists(cookie_file):
        try:
            cookiejar.load()
        # in case file is empty
        except Exception:
            pass

    browser = mechanicalsoup.StatefulBrowser()
    # ? error handling here?
    browser.set_cookiejar(cookiejar)

    return browser, cookiejar


def cache_files(upload_map, config):
    """
    Loads filenames into memory, along with setting up
    appropriate objects to generate URLs and hashes as required.

    Arguments:
        upload_map: custom upload map
        config: configuration for this run

    Returns:
        cache: dictionary with html, css, js and other file objects
    """

    cache = {
        'html': {},
        'css': {},
        'js': {},
        'other': {}
    }

    # for each file in src_dir
    for root, _, files in os.walk(config['src_dir']):
        for filename in files:

            # Store path and extension
            infile = (Path(root) / Path(filename)).relative_to(config['src_dir'])
            extension = infile.suffix[1:].lower()

            # create appropriate file object
            # file objects contain corresponding paths and URLs
            if extension == 'html':
                file_object = HTMLfile(infile, config)
                cache['html'][file_object.path] = file_object

            elif extension == 'css':
                file_object = CSSfile(infile, config)
                cache['css'][file_object.path] = file_object

            elif extension == 'js':
                file_object = JSfile(infile, config)
                cache['js'][file_object.path] = file_object

            elif extension.lower() in ['png', 'gif', 'jpg', 'jpeg', 'pdf', 'ppt', 'txt',
                                       'zip', 'mp3', 'mp4', 'webm', 'mov', 'swf', 'xls',
                                       'xlsx', 'docx', 'pptx', 'csv', 'm', 'ogg', 'gb',
                                       'tif', 'tiff', 'fcs', 'otf', 'eot', 'ttf', 'woff', 'svg']:

                file_object = OtherFile(infile, config)
                cache['other'][file_object.path] = file_object

            else:
                file_object = None  # just to shut up lintian
                logger.info(f'{infile} has an unsupported file extension. Skipping.')
                # ? Do we want to support other text files?
                # Team lead says no.

            if extension in ['html', 'css', 'js']:
                if str(file_object.path) not in upload_map[extension].keys():
                    upload_map[extension][str(file_object.path)] = {
                        'md5': '',
                        'link_URL': file_object.link_URL
                    }

    return cache


def upload_assets(other_files, browser, upload_map):
    """"
    Uploads all files and stores URLs in upload_map.

    Arguments:
        other_files: dictionary containing OtherFile objects
        browser: mechanicalsoup.StatefulBrowser instance
        upload_map: custom upload map

    Returns:
        True if successful
        Exits if fails
    """
    # files have to be uploaded before everything else because
    # the URLs iGEM assigns are random
    for path in other_files.keys():
        file_object = other_files[path]
        uploaded = False  # flag to keep track of current file upload

        # check if the file has already been uploaded
        for asset_path in upload_map['assets'].keys():

            if asset_path == str(path):
                asset = upload_map['assets'][asset_path]
                if file_object.md5_hash == asset['md5']:
                    # ? Can't do anything about renames. iGEM API doesn't allow.
                    # ? Can find the previous URL and use that itself
                    # ? but is it worth the effort?
                    # Team lead says no.
                    pass
                else:
                    # if file has changed, upload file and update hash
                    successful = iGEM_upload_file(browser, file_object)
                    if not successful:
                        # print upload map to save the current state
                        write_upload_map(upload_map)
                        message = f'Failed to upload {str(file_object.path)}. ' + \
                            'The current upload map has been saved. ' + \
                            'You will not have to upload everything again.'
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
            successful = iGEM_upload_file(browser, file_object)
            if not successful:
                # print upload map to save the current state
                write_upload_map(upload_map)
                message = f'Failed to upload {str(file_object.path)}. '
                message += 'The current upload map has been saved. '
                message += 'You will not have to upload everything again.'
                logger.debug(message, exc_info=True)
                logger.error(message)
                raise SystemExit

            upload_map['assets'][str(path)] = {
                'link_URL': file_object.upload_URL,
                'md5': file_object.md5_hash,
                'upload_filename': file_object.upload_filename
            }

    return True


def build_and_upload(files, browser, config, upload_map):
    """
    Replaces URLs in files and uploads changed files.

    Arguments:
        files: Custom file cache
        browser: mechanicalsoup.StatefulBrowser instance
        config: Configuration for this run
        upload_map: custom upload map

    Returns:
        Nothing
    """

    for file_dictionary in [files['html'], files['css'], files['js']]:
        for path in file_dictionary.keys():
            file_object = file_dictionary[path]
            path_str = str(file_object.path)
            ext = file_object.extension

            # open file
            try:
                with open(file_object.src_path, 'r') as file:
                    contents = file.read()
            except Exception:
                message = f'Could not open/read {file_object.path}. Skipping.'
                logger.error(message)
                continue  # FIXME Can this be improved?

            processed = None  # just so the linter doesn't freak out
            # parse and modify contents
            if ext == 'html':
                processed = HTMLparser(
                    config, file_object.path, contents, upload_map)
            elif ext == 'css':
                processed = CSSparser(
                    config, file_object.path, contents, upload_map)
            elif ext == 'js':
                processed = JSparser(contents)

            # calculate and store md5 hash of the modified contents
            build_hash = md5(processed.encode('utf-8')).hexdigest()

            if upload_map[ext][path_str]['md5'] == build_hash:
                message = f'Contents of {file_object.path} have been uploaded previously. Skipping.'
                logger.info(message)
            else:
                upload_map[ext][path_str]['md5'] = build_hash
                build_path = file_object.build_path
                try:
                    # create directory if doesn't exist
                    if not os.path.isdir(build_path.parent):
                        os.makedirs(build_path.parent)
                    # and write the processed contents
                    with open(build_path, 'w') as file:
                        file.write(processed)
                except Exception:
                    message = f"Couldn not write {str(file_object.build_path)}. Skipping."
                    logger.info(message)
                    continue
                    # FIXME Can this be improved?

                # upload
                successful = iGEM_upload_page(browser, processed, file_object.upload_URL)
                if not successful:
                    message = f'Could not upload {str(file_object.path)}. Skipping.'
                    logger.info(message)
                    continue
                    # FIXME Can this be improved?
