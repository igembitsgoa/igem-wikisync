import re

from bs4 import BeautifulSoup
from jsmin import jsmin

from igem_wikisync.path import iGEM_URL

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

    # TODO: Replace URLs for AJAX loads as well
    # TODO: img srcset

    for (tag_name, attr) in queries:
        query = soup.findAll(tag_name, attrs={attr: True, 'data-nosub': False})
        for tag in query:
            tag[attr] = iGEM_URL(config, path, upload_map, tag[attr])
            # TODO: Add error handling

    inline_styles = soup.findAll('style')
    for style in inline_styles:
        style.string = CSSparser(config, path, style.string, upload_map)
        pass

    contents = str(soup)
    return contents


def CSSparser(config, path, contents, upload_map):

    # TODO: Replace URLs in image(), image-set() and cross-fade()

    css = contents

    # 1) Find all css links
    exp = r'url\([\'\"]?([^\)\'\"]*)[\'\"]?\)'
    links = re.findall(exp, css)

    for i in range(len(links)):
        links[i] = links[i].split('?')[0]
        links[i] = links[i].split('#')[0]

    # 2) Clear all duplicates
    links = list(dict.fromkeys(links))

    # 3) Replace all links with the absolute path
    for link in links:
        css = css.replace(link, iGEM_URL(config, path, upload_map, link))

    return css


def JSparser(contents):

    contents = jsmin(contents)
    # TODO: URL replacement in JS
    return contents
