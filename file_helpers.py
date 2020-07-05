from bs4 import BeautifulSoup
from helpers import URLreplace, getUploadURL
from jsmin import jsmin
import cssutils
import os
import pathlib

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
    
