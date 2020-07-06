import os
import re
import ssl
import shutil
import yaml
from pathlib import Path
import cssutils
from jsmin import jsmin
import mechanicalsoup
from bs4 import BeautifulSoup
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

from browser_helpers import iGEMlogin, iGEMupload
from file_helpers import BaseFile, HTMLfile, CSSfile, JSfile, HTMLhandler, CSShandler, JShandler
from helpers import getUploadURL, URLreplace

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

    # for each file in src_dir
    for root, directories, files in os.walk(src_dir):
        for filename in files:

            infile = Path(root) / Path(filename)
            if "html" in infile.suffix:
                current_file = HTMLfile(infile, config)
            elif "css" in infile.suffix:
                current_file = CSSfile(infile, config)
            elif "js" in infile.suffix:
                current_file = JSfile(infile, config)
            else:
                current_file = BaseFile(infile, config)

            print("hello")
            # get infile, outfile and upload URLs
            # relative = ""
            # outfile = build_dir + relative
            # uploadURL = getUploadURL(team, relative)
            # extension = os.path.splitext(filename)[1][1:].lower()
            # out_dir = os.path.dirname(outfile)

            # # if file is not a text file, copy and continue
            # if extension not in ["html", "css", "scss", "js"]:
            #     # create directory if doesn't exist
            #     if not os.path.isdir(out_dir):
            #         os.makedirs(out_dir)
            #     shutil.copyfile(infile, outfile)
            #     continue

            # # read file
            # with open(infile, 'r') as file:
            #     contents = file.read()

            # # process contents according to file extension
            # if extension == 'html':
            #     contents = HTMLhandler(team, contents)
            # elif extension == 'css':
            #     contents = CSShandler(team, contents, infile, src_dir)
            # elif extension == 'js':
            #     contents = JShandler(team, contents)

            # if not os.path.exists(os.path.dirname(outfile)):
            #     os.makedirs(os.path.dirname(outfile))
            # with open(outfile, 'w') as file:
            #     file.write(contents)
            # # print('Wrote', infile, 'to', outfile)

    # get iGEM credentials
    username = os.environ.get('IGEM_USERNAME')
    password = os.environ.get('IGEM_PASSWORD')

    # declare a global browser instance
    browser = mechanicalsoup.StatefulBrowser()

    # login to iGEM
    response = iGEMlogin(browser, username, password)
    # print(response)

    # for each file in build_dir
    for root, directories, files in os.walk(build_dir):
        for filename in files:

            # get infile, outfile and upload URLs
            outfile = root + '/' + filename
            relative = infile[len(build_dir):]
            uploadURL = getUploadURL(team, relative)

            iGEMupload(browser, outfile, uploadURL)
            # print('Uploaded', infile, 'to', uploadURL)


if __name__ == '__main__':
    main()
