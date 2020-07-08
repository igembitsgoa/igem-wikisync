from bs4 import BeautifulSoup
from helpers import is_relative, iGEM_URL, resolve_relative_URL
import cssutils
from pathlib import Path
import os
from jsmin import jsmin

# process HTML files


def HTMLparser(config, path, contents, upload_map):

    # https://stackoverflow.com/questions/2725156/complete-list-of-html-tag-attributes-which-have-a-url-value

    soup = BeautifulSoup(contents, 'html5lib')

    queries = [('link', 'href'), ('script', 'src'), ('a', 'href'),
               ('applet', 'codebase'), ('area', 'href'), ('base', 'href'),
               ('blockquote', 'cite'), ('body', 'background'), ('del', 'cite'),
               ('form', 'action'), ('frame', 'longdesc'), ('frame', 'src'),
               ('head', 'profile'), ('iframe', 'longdesc'), ('iframe', 'src'),
               ('img', 'longdesc'), ('img', 'src'), ('img', 'usemap'),
               ('input', 'src'), ('input', 'usemap'), ('ins', 'cite'),
               ('object', 'classid'), ('object', 'codebase'), ('object', 'data'),
               ('object', 'usemap'), ('q', 'cite'), ('audio', 'src'),
               ('button', 'formaction'), ('command', 'icon'), ('embed', 'src'),
               ('html', 'manifest'), ('input', 'formaction'), ('source', 'src'),
               ('track', 'src'), ('video', 'poster'), ('video', 'src')]

    for (tag_name, attr) in queries:
        query = soup.findAll(tag_name, attrs={attr: True})
        for tag in query:

            tag[attr] = iGEM_URL(config, path, upload_map, tag[attr])

    contents = str(soup)
    return contents


def CSSparser(config, path, contents, upload_map):
    cssutils.ser.prefs.useMinified()
    sheet = cssutils.parseString(contents)

    def replacer(url:str) -> str:
        return iGEM_URL(config, path, upload_map, url)

    cssutils.replaceUrls(sheet, replacer=replacer)
    contents = sheet.cssText.decode("utf-8")
    return contents


def JSparser(config, path, contents):

    contents = jsmin(contents)
    return contents
