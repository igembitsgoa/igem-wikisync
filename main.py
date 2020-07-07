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

# https://bitbucket.org/cthedot/cssutils/issues/60/using-units-of-rem-produces-an-invalid
from cssutils import profile
profile._MACROS['length'] = r'0|{num}(em|ex|px|in|cm|mm|pt|pc|q|ch|rem|vw|vh|vmin|vmax)'
profile._MACROS['positivelength'] = r'0|{positivenum}(em|ex|px|in|cm|mm|pt|pc|q|ch|rem|vw|vh|vmin|vmax)'
profile._MACROS['angle'] = r'0|{num}(deg|grad|rad|turn)'
profile._resetProperties()


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

    # clear build_dir
    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir)
        os.mkdir(build_dir)

    # get iGEM credentials
    username = os.environ.get('IGEM_USERNAME')
    password = os.environ.get('IGEM_PASSWORD')

    # declare a global browser instance
    browser = mechanicalsoup.StatefulBrowser()

    # login to iGEM
    response = iGEM_login(browser, username, password)
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

            if extension == "html":

                file_object = HTMLfile(infile, config)

                HTMLfiles[file_object.path] = file_object

            elif extension == "css":

                file_object = CSSfile(infile, config)

                CSSfiles[file_object.path] = file_object

            elif extension == "js":

                file_object = JSfile(infile, config)

                JSfiles[file_object.path] = file_object

            elif extension in ['png', 'gif', 'jpg', 'jpeg', 'pdf', 'ppt', 'txt',
                               'zip', 'mp3', 'mp4', 'webm', 'mov', 'swf', 'xls',
                               'xlsx', 'docx', 'pptx', 'csv', 'm', 'ogg', 'gb',
                               'tif', 'tiff', 'fcs', 'otf', 'eot', 'ttf', 'woff', 'svg']:

                file_object = OtherFile(infile, config)

                if file_object.upload_filename in OtherFiles.keys():
                    print('You have multiple files named', file_object.filename)

                OtherFiles[file_object.upload_filename] = file_object

            else:
                print(infile, "has an unsupported file extension. Skipping.")

    # check for upload map
    if os.path.isfile('uploadmap.yml'):
        with open('uploadmap.yml', 'r') as file:
            uploadmap = yaml.safe_load(file)
    else:
        uploadmap = {
            'assets': []
        }

    if uploadmap is None:
        uploadmap = {
            'assets': []
        }
    elif 'assets' not in uploadmap.keys():
        uploadmap['assets'] = []

    # Upload all assets and create a map
    # for file in OtherFiles.keys()
    for filename in OtherFiles.keys():
        file_object = OtherFiles[filename]
        uploaded = False  # flag to keep track of current file upload

        for asset in uploadmap['assets']:

            if asset['upload_filename'] == str(file_object.upload_filename):
                if file_object.md5_hash == asset['md5']:
                    uploaded = True
                else:
                    # upload file and update hash
                    response = iGEM_upload_file(browser, file_object)
                    asset['md5'] = file_object.md5_hash
                    asset['url'] = file_object.upload_URL
                    uploaded = True  # repeated here because error handling has to be added
                break

        if not uploaded:
            response = iGEM_upload_file(browser, file_object)
            uploadmap['assets'].append({
                'path': str(file_object.path),
                'url': file_object.upload_URL,
                'md5': file_object.md5_hash,
                'upload_filename': file_object.upload_filename
            })

    with open('uploadmap.yml', 'w') as file:
        yaml.dump(uploadmap, file, sort_keys=True)

    # for file_list in [HTMLfiles, CSSfiles, JSfiles]:

    # for file_object in HTMLfiles:

    #     contents = file_object.parse_file()
    #     build_path = file_object.build_path

    #     # create directory if doesn't exist
    #     if not os.path.isdir(build_path.parent):
    #         os.makedirs(build_path.parent)
    #     with open(build_path, 'w') as f:
    #         f.write(contents)

    # if not os.path.exists(os.path.dirname(outfile)):
    #     os.makedirs(os.path.dirname(outfile))

    # # for each file in build_dir
    # for root, _, files in os.walk(build_dir):
    #     for filename in files:

    #         # get infile, outfile and upload URLs
    #         outfile = root + '/' + filename
    #         relative = infile[len(build_dir):]
    #         uploadURL = getUploadURL(team, relative)

    #         iGEMupload(browser, outfile, uploadURL)
    #         # print('Uploaded', infile, 'to', uploadURL)


if __name__ == '__main__':
    main()
