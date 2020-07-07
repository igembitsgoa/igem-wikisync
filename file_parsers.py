from bs4 import BeautifulSoup
from helpers import is_relative, iGEM_URL, resolve_relative_URL
import cssutils
from pathlib import Path
import os
from jsmin import jsmin

# process HTML files


def HTMLparser(config, path, contents):

    # https://stackoverflow.com/questions/2725156/complete-list-of-html-tag-attributes-which-have-a-url-value

    soup = BeautifulSoup(contents, 'html5lib')

    # <a href=url>
    # <applet codebase=url>
    # <area href=url>
    # <base href=url>
    # <blockquote cite=url>
    # <body background=url>
    # <del cite=url>
    # <form action=url>
    # <frame longdesc=url> and <frame src=url>
    # <head profile=url>
    # <iframe longdesc=url> and <iframe src=url>
    # <img longdesc=url> and <img src=url> and <img usemap=url>
    # <input src=url> and <input usemap=url>
    # <ins cite=url>
    # <link href=url>
    # <object classid=url> and <object codebase=url> and <object data=url> and <object usemap=url>
    # <q cite=url>
    # <script src=url>
    # <audio src=url>
    # <button formaction=url>
    # <command icon=url>
    # <embed src=url>
    # <html manifest=url>
    # <input formaction=url>
    # <source src=url>
    # <track src=url>
    # <video poster=url> and <video src=url>

    queries = [('link', 'href'),
               ('script', 'src')]

    for (tag_name, attr) in queries:
        query = soup.findAll(tag_name)
        for tag in query:
            if is_relative(tag[attr]):
                old = tag[attr]
                resolved = resolve_relative_URL(config, path.parent, tag[attr])

                # check if file exists
                filepath = config['src_dir'] / resolved
                if not os.path.isfile(filepath):
                    print("Warning:", filepath, "is referenced in",
                          config['src_dir'] / path, "but was not found.")

                tag[attr] = iGEM_URL(config, resolved)
                print(old, "was changed to", tag[attr])
            # print(css_tag['href'])

    contents = str(soup)
    return contents


def CSSparser(config, path, contents):
    cssutils.ser.prefs.useMinified()
    sheet = cssutils.parseString(contents)
    absoluteSourceDir = Path('.').resolve() / src_dir

    def replacer(url):
        p = Path(url)

        absoluteLocalURL = (os.path.dirname(cssFilePath) / p).resolve()
        relativeToSourceDir = absoluteLocalURL.relative_to(absoluteSourceDir)

        return str(relativeToSourceDir)

    cssutils.replaceUrls(sheet, replacer=replacer)
    contents = sheet.cssText.decode("utf-8")
    return contents


def JSparser(config, path, contents):

    contents = jsmin(contents)
    return contents
