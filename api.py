import os
import re
import ssl
import shutil
import yaml
import pathlib
import cssutils
import mechanicalsoup
from jsmin import jsmin
from datetime import datetime
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

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

            # get infile, outfile and upload URLs
            infile = root + '/' + filename
            relative = infile[len(src_dir):]
            outfile = build_dir + relative
            uploadURL = getUploadURL(team, relative)
            extension = os.path.splitext(filename)[1][1:].lower()
            out_dir = os.path.dirname(outfile) 

            # if file is not a text file, copy and continue
            if extension not in ["html", "css", "scss", "js"]:
                # create directory if doesn't exist
                if not os.path.isdir(out_dir):
                    os.makedirs(out_dir)
                shutil.copyfile(infile, outfile)
                continue

            # read file
            with open(infile, 'r') as file:
                contents = file.read()
            
            # process contents according to file extension
            if extension == 'html':
                contents = HTMLhandler(team, contents)
            elif extension == 'css':
                contents = CSShandler(team, contents, infile, src_dir)
            elif extension == 'js':
                contents = JShandler(team, contents)

            if not os.path.exists(os.path.dirname(outfile)):
                os.makedirs(os.path.dirname(outfile))
            with open(outfile, 'w') as file:
                file.write(contents)
            # print('Wrote', infile, 'to', outfile)
    
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

def iGEMlogin(browser, username, password):

    return "No"

    browser.open("https://igem.org/Login2")
    browser.select_form('form[method="post"]')
    browser["username"] = username
    browser["password"] = password
    response = browser.submit_selected()

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.text

def getUploadURL(team, relative):
    if re.match('http', relative):
        return relative
    else:
        extension = os.path.splitext(relative)[1][1:].upper()
        if extension == 'HTML':
            # remove '/index.html' from the end
            if relative.endswith('/index.html'):
                relative = relative[:-11]
            return 'https://2020.igem.org/wiki/index.php?title=Team:' + team + relative + '&action=edit'
        elif extension == 'CSS' or extension == 'JS': 
            final = os.path.splitext(relative)[0] + extension
            return 'https://2020.igem.org/wiki/index.php?title=Template:' + team + final + '&action=edit'

# process HTML files
def HTMLhandler(team, contents):
    soup = BeautifulSoup(contents, 'html.parser')

    css_tags = soup.findAll('link')
    for css_tag in css_tags:
        css_tag['href'] = URLreplace(team, css_tag['href'])
        # print(css_tag['href'])

    js_tags = soup.findAll('script')
    for js_tag in js_tags:
        js_tag['src'] = URLreplace(team, js_tag['src'])
        # print(js_tag['src'])

    contents = str(soup)
    return contents


def CSShandler(team, contents, cssFilePath, src_dir):
    cssutils.ser.prefs.useMinified()    
    sheet = cssutils.parseString(contents)
    absoluteSourceDir = pathlib.Path('.').resolve() / src_dir


    def replacer(url):
        p = pathlib.Path(url)

        absoluteLocalURL = (os.path.dirname(cssFilePath) / p).resolve()
        relativeToSourceDir = absoluteLocalURL.relative_to(absoluteSourceDir)

        return str(relativeToSourceDir)

    cssutils.replaceUrls(sheet, replacer=replacer)
    contents = sheet.cssText.decode("utf-8")
    return contents

def JShandler(team, contents):
    
    contents = jsmin(contents)
    return contents
    
def URLreplace(team, relative):
    if re.match('http', relative):
        return relative
    
    extension = os.path.splitext(relative)[1][1:].upper()
    
    if extension == 'CSS':
        filetype = 'css'
    elif extension == 'JS':
        filetype = 'javascript'
    
    absolute = os.path.splitext(relative)[0] + extension
    if absolute[0] != '/':
        absolute = '/' + absolute
    absolute = 'https://2020.igem.org/Template:' + team + absolute + '?action=raw&ctype=text/' + filetype
    
    return absolute

def iGEMupload(browser, outfile, uploadURL):

    return "no"

    with open(outfile, 'r') as file:
        contents = file.read()
    browser.open(uploadURL)
    
    browser.select_form('form')
    browser['wpTextbox1'] = contents
    browser['wpSummary'] = 'Uploaded at ' + str(datetime.now())
    response = browser.submit_selected()

    return response.text

if __name__ == '__main__':
    main()
