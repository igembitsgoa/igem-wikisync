import os
import sys
import shutil
from datetime import date
from hashlib import md5
from http.cookiejar import LWPCookieJar
from pathlib import Path

import mechanicalsoup
import yaml

from igem_wikisync.browser import iGEM_login
from igem_wikisync.browser import iGEM_upload_file
from igem_wikisync.browser import iGEM_upload_page
from igem_wikisync.files import CSSfile
from igem_wikisync.files import HTMLfile
from igem_wikisync.files import JSfile
from igem_wikisync.files import OtherFile
from igem_wikisync.logger import logger
from igem_wikisync.parsers import CSSparser
from igem_wikisync.parsers import HTMLparser
from igem_wikisync.parsers import JSparser

# pylint: disable=too-many-instance-attributes, fixme


def run(team: str,
        src_dir: str,
        build_dir: str,
        year=date.today().year,
        silence_warnings=False):
    '''
    Runs iGEM-WikiSync and uploads all files to iGEM servers
    while replacing relative URLs with those on the iGEM server.

    Mandatory Arguments:
        team: iGEM Team Name
        src_dir: Path to the folder where the source files are present
        build_dir: Path to the folder where the built files will be stored before uploading

    Optional Arguments:
        year: Subdomain for igem.org. Current year by default.
        silence_warnings: Broken link warnings are not printed to console if true. The log still contains everything.

    Returns:
        1: Incorrect input in function call.
        2: Connection problem.
        3: Invalid upload map.
        4: Failed to write/upload file.
    '''

    # * 1. CHECK AND FORMAT INPUTS
    if team is None or not isinstance(team, str):
        logger.critical('Please specify your team name.')
        sys.exit(1)

    if src_dir is None or not isinstance(src_dir, str):
        logger.critical('Please specify where your code is stored ' +
                        'using the src_dir argument.')
        sys.exit(1)

    if build_dir is None or not isinstance(build_dir, str):
        logger.critical('Please specify where your code should be temporarily stored ' +
                        'using the build_dir argument.')
        sys.exit(1)

    if not isinstance(year, int) or len(str(year)) > 4:
        logger.critical('Year should be a four digit integer.')
        sys.exit(1)

    if not isinstance(silence_warnings, bool):
        logger.critical('silence_warnings must have a boolean value.')
        sys.exit(1)

    config = {
        'team':      team,
        'src_dir':   src_dir,
        'build_dir': build_dir,
        'year': str(year),
        'silence_warnings': silence_warnings
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
        'password': os.environ.get('IGEM_PASSWORD')
    }

    # * 5. Load/create cookie file
    browser, cookiejar = get_browser_with_cookies()

    # * 6. Login to iGEM
    login = iGEM_login(browser, credentials, config)
    if not login:
        message = 'Failed to login.'
        logger.critical(message)
        sys.exit(2)

    # * 7. Save cookies
    # TODO: check if this works, might not
    cookiejar.save()

    # * 8. Cache files
    files = cache_files(upload_map, config)

    # * 9. Upload all assets and create a map
    uploaded_assets = upload_and_write_assets(files['other'], browser, upload_map, config)

    # * 10. write upload map just in case
    # things go wrong while dealing with code
    write_upload_map(upload_map)

    # * 11. Build files and upload changed files
    uploaded_code = build_and_upload(files, browser, config, upload_map)

    # * 12. Write final upload map
    write_upload_map(upload_map)

    print_summary(uploaded_assets, uploaded_code)


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
            logger.critical('upload_map.yml exists but could not be opened. Please try again.')
            sys.exit(3)

        if isinstance(upload_map, type(None)):
            upload_map = {}

        # make sure upload map has all the keys
        for key in ['assets', 'html', 'css', 'js']:
            if key not in upload_map.keys() or isinstance(upload_map[key], type(None)):
                upload_map[key] = {}
            elif not isinstance(upload_map[key], dict):
                logger.critical('upload_map.yml has an invalid format.')
                logger.critical('Please fix/delete the file and run the program again.')
                sys.exit(3)

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

    cookie_file = 'wikisync.cookies'
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

                # make sure file path start with 'assets'
                if len(str(infile)) < 7 or infile.parts[0] != 'assets':
                    logger.error(f'{infile} is an {extension} file outside the "assets" folder. Skipping.')
                    continue

                # make sure file size is within limits
                elif (config['src_dir'] / infile).stat().st_size >= 1000000:
                    logger.error(f'{infile} is larger than the 100MB file limit. Skipping.')
                    continue
                # create OtherFile
                else:
                    file_object = OtherFile(infile, config)

                    if len(file_object.upload_filename) < 240:
                        cache['other'][file_object.path] = file_object
                    else:
                        logger.error(f'{infile}: Upload filename too large. Skipping.')
                        logger.error('Please do not nest assets too deep and take a look at our docs to see how WikiSync renames files.')
                        continue

            else:
                logger.error(f'{infile} has an unsupported file extension. Skipping.')
                continue

            if extension in ['html', 'css', 'js']:
                if str(file_object.path) not in upload_map[extension].keys():
                    upload_map[extension][str(file_object.path)] = {
                        'md5': '',
                        'link_URL': file_object.link_URL
                    }

    return cache


def upload_and_write_assets(other_files, browser, upload_map, config):
    """"
    Uploads and writes all files and stores URLs in upload_map.

    Arguments:
        other_files: dictionary containing OtherFile objects
        browser: mechanicalsoup.StatefulBrowser instance
        upload_map: custom upload map
        config: custom configuration options

    Returns:
        Number of files uploaded

    Raises:
        SystemExit on failure
    """

    # count the number of files uploaded
    counter = 0

    # files have to be uploaded before everything else because
    # the URLs iGEM assigns are random
    for path in other_files.keys():
        file_object = other_files[path]

        # flag to see if file has already been uploaded
        uploaded = False

        # check if the file has already been uploaded
        for asset_path in upload_map['assets'].keys():

            # if current path matches stored path
            if asset_path == str(path):
                asset = upload_map['assets'][asset_path]
                # and the md5 hash is also the same
                if file_object.md5_hash == asset['md5']:
                    # the file has already been uploaded
                    uploaded = True
                    break
                else:
                    # the file path matches, but the md5 hash doesn't
                    # this means the file has changed
                    uploaded = False
                    break

        # if new file
        if not uploaded:
            # write to build_dir
            try:
                # create directory if doesn't exist
                if not os.path.isdir(file_object.build_path.parent):
                    os.makedirs(file_object.build_path.parent)
                shutil.copyfile(file_object.src_path, file_object.build_path.parent / file_object.upload_filename)
            except Exception:
                # print upload map to save the current state
                write_upload_map(upload_map)
                message = f'Failed to write {str(file_object.path)} to build_dir. ' + \
                    'The current upload map has been saved. ' + \
                    'You will not have to upload everything again.'
                logger.debug(message, exc_info=True)
                logger.critical(message)
                sys.exit(4)

            successful = iGEM_upload_file(browser, file_object, config['year'])
            if not successful:
                # print upload map to save the current state
                write_upload_map(upload_map)
                message = f'Failed to upload {str(file_object.path)}. '
                message += 'The current upload map has been saved. '
                message += 'You will not have to upload everything again.'
                logger.debug(message, exc_info=True)
                logger.critical(message)
                sys.exit(4)
            else:
                counter += 1

            if str(path) in upload_map['assets'].keys():
                upload_map['assets'][str(path)]['md5'] = file_object.md5_hash
                upload_map['assets'][str(path)]['link_URL'] = file_object.link_URL
            else:
                upload_map['assets'][str(path)] = {
                    'link_URL': file_object.link_URL,
                    'md5': file_object.md5_hash,
                    'upload_filename': file_object.upload_filename
                }

    return counter


def build_and_upload(files, browser, config, upload_map):
    """
    Replaces URLs in files and uploads changed files.

    Arguments:
        files: Custom file cache
        browser: mechanicalsoup.StatefulBrowser instance
        config: Configuration for this run
        upload_map: custom upload map

    Returns:
        Dictionary with no. of 'html', 'css' and 'js' files uploaded
    """

    counter = {
        'html': 0,
        'css': 0,
        'js': 0,
    }

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
                    logger.error(message)
                    continue
                    # FIXME Can this be improved?

                # upload
                successful = iGEM_upload_page(browser, processed, file_object.upload_URL)
                if not successful:
                    message = f'Could not upload {str(file_object.path)}. Skipping.'
                    logger.error(message)
                    continue
                    # FIXME Can this be improved?
                else:
                    counter[ext] += 1

    return counter


def print_summary(assets, code):

    total_count = assets + code['html'] + code['css'] + code['js']

    if total_count == 0:
        print('WikiSync did not find any changes from the previous run. No files were uploaded.')
    elif total_count == assets:
        print(f"Done! Successfully uploaded {assets} assets.")
    elif total_count == code['html']:
        print(f"Done! Successfully uploaded {code['html']} HTML files.")
    elif total_count == code['css']:
        print(f"Done! Successfully uploaded {code['css']} stylesheets.")
    elif total_count == code['js']:
        print(f"Done! Successfully uploaded {code['js']} JS scripts.")
    else:
        print("Done! Successfully uploaded:")
        if assets != 0:
            print(f"    {assets} assets")
        if code['html'] != 0:
            print(f"    {code['html']} HTML files")
        if code['css'] != 0:
            print(f"    {code['css']} stylesheets")
        if code['js'] != 0:
            print(f"    {code['js']} JS scripts")

    print("Please look at the log for more details.")
