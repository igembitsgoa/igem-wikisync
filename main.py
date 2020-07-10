import os
import ssl
import shutil
import yaml
from pathlib import Path
import mechanicalsoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

from browser_helpers import iGEM_login, iGEM_upload_page, iGEM_upload_file
from file_helpers import HTMLfile, CSSfile, JSfile, OtherFile
from code_parsers import CSSparser, HTMLparser, JSparser
from hashlib import md5

# https://bitbucket.org/cthedot/cssutils/issues/60/using-units-of-rem-produces-an-invalid
from cssutils import profile
profile._MACROS['length'] = r'0|{num}(em|ex|px|in|cm|mm|pt|pc|q|ch|rem|vw|vh|vmin|vmax)'
profile._MACROS['positivelength'] = r'0|{positivenum}(em|ex|px|in|cm|mm|pt|pc|q|ch|rem|vw|vh|vmin|vmax)'
profile._MACROS['angle'] = r'0|{num}(deg|grad|rad|turn)'
profile._resetProperties()


# For TLSv1.0 support
# https://lukasa.co.uk/2013/01/Choosing_SSL_Version_In_Requests/
class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


def main():

    # read config file
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

    team = config['team']
    src_dir = config['src_dir']
    build_dir = config['build_dir']

    # load or create upload_map
    upload_map = None
    if os.path.isfile('upload_map.yml'):
        with open('upload_map.yml', 'r') as file:
            upload_map = yaml.safe_load(file)

    if upload_map is None:
        upload_map = {
            'assets': {},
            'html': {},
            'css': {},
            'js': {}
        }

    if 'assets' not in upload_map.keys():
        upload_map['assets'] = {}
    if 'html' not in upload_map.keys():
        upload_map['html'] = {}
    if 'css' not in upload_map.keys():
        upload_map['css'] = {}
    if 'js' not in upload_map.keys():
        upload_map['js'] = {}

    # clear build_dir
    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir)
        os.mkdir(build_dir)

    # get iGEM credentials
    credentials = {
        'username': os.environ.get('IGEM_USERNAME'),
        'password': os.environ.get('IGEM_PASSWORD')
    }

    # declare a global browser instance
    browser = mechanicalsoup.StatefulBrowser()

    # login to iGEM
    response = iGEM_login(browser, credentials)
    print(response)

    # storage
    HTMLfiles = {}
    CSSfiles = {}
    JSfiles = {}
    OtherFiles = {}

    # for each file in src_dir
    for root, _, files in os.walk(src_dir):
        for filename in files:

            infile = Path(root) / Path(filename)
            extension = infile.suffix[1:]

            # create appropriate file object
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
                print(infile, "has an unsupported file extension. Skipping.")

    # Upload all assets and create a map
    for path in OtherFiles.keys():
        file_object = OtherFiles[path]
        uploaded = False  # flag to keep track of current file upload

        for asset_path in upload_map['assets'].keys():

            if asset_path == str(path):
                asset = upload_map['assets'][asset_path]
                if file_object.md5_hash == asset['md5']:
                    pass
                else:
                    # upload file and update hash
                    response = iGEM_upload_file(
                        browser, credentials, file_object)
                    asset['md5'] = file_object.md5_hash
                    asset['link_URL'] = file_object.upload_URL
                    # add error handling
                uploaded = True
                break

        if not uploaded:
            response = iGEM_upload_file(browser, credentials, file_object)
            upload_map['assets'][str(path)] = {
                'link_URL': file_object.upload_URL,
                'md5': file_object.md5_hash,
                'upload_filename': file_object.upload_filename
            }

    with open('upload_map_files.yml', 'w') as file:
        yaml.dump(upload_map, file, sort_keys=True)

    for file_dictionary in [HTMLfiles, CSSfiles, JSfiles]:
        for path in file_dictionary.keys():
            file_object = file_dictionary[path]
            path_str = str(file_object.path)
            ext = file_object.extension

            # open file
            with open(file_object.src_path, 'r') as file:
                contents = file.read()

            processed = contents
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
                print("Contents of", file_object.path,
                      "have been uploaded previously. Skipping.")
            else:
                upload_map[ext][path_str]['md5'] = build_hash
                build_path = file_object.build_path
                # create directory if doesn't exist
                if not os.path.isdir(build_path.parent):
                    os.makedirs(build_path.parent)
                with open(build_path, 'w') as f:
                    f.write(processed)

                # upload
                response = iGEM_upload_page(
                    browser, credentials, processed, file_object.upload_URL)

    with open('upload_map.yml', 'w') as file:
        yaml.dump(upload_map, file, sort_keys=True)


if __name__ == '__main__':
    main()
