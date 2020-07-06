import os
from pathlib import Path
import cssutils
from jsmin import jsmin
from bs4 import BeautifulSoup
from helpers import URLreplace, getUploadURL


class BaseFile:
    def __init__(self, path, config):
        self._config = config

        self._path = Path(path).relative_to(self._config['src_dir'])
        self._stem = str(self._path.stem)
        self._extension = str(self._path.suffix[1:])
        self._filename = str(self._stem + '.' + self._extension)
        self._parent = self._path.parent
        self._build_path = self._config["build_dir"] / self._path

    @property
    def path(self):
        """ Returns path of the file relative to src_dir. """
        return self._path

    @property
    def filename(self):
        ''' Returns filename with extension. '''
        return self._filename

    @property
    def extension(self):
        ''' Returns extension of the file. '''
        return self._extension

    @property
    def parent(self):
        ''' Returns path without the filename and terminal /. '''
        return self._parent

    @property
    def build_path(self):
        ''' Returns build path. '''
        return self._build_path


class HTMLfile(BaseFile):
    def __init__(self, path, config):
        BaseFile.__init__(self, path, config)
        self._upload_path = self._generate_upload_path()
        self._upload_URL = self._generate_upload_URL()
        self._link_URL = self._generate_link_URL()

    @property
    def upload_URL(self):
        return self._upload_URL

    @property
    def link_URL(self):
        return self._link_URL

    def _generate_upload_path(self):
        """
            Returns upload path, which is the part of the URL after team name
            but before & and all. Includes / if required.
        """
        # remove /index.html
        upload_path = str(self.path.parent)

        if upload_path == ".":
            return ""
        else:
            return "/" + upload_path

    def _generate_upload_URL(self):
        """
            Returns the URL of the iGEM page where this file can be uploaded.
            Private function. Use upload_URL to access instead.
        """
        return 'https://2020.igem.org/wiki/index.php?title=Team:' + \
            self._config["team"] + self._upload_path + '&action=edit'

    def _generate_link_URL(self):
        """
            Returns the iGEM URL where this page will be found and can be linked to.
        """
        return 'https://2020.igem.org/Team:' + self._config['team'] + \
            self._upload_path


class CSSfile(BaseFile):
    def __init__(self, path, config):
        BaseFile.__init__(self, path, config)
        self._upload_path = self._generate_upload_path()
        self._upload_URL = self._generate_upload_URL()
        self._link_URL = self._generate_link_URL()

    @property
    def upload_URL(self):
        return self._upload_URL

    @property
    def link_URL(self):
        return self._link_URL

    def _generate_upload_path(self):
        """
            Returns upload path, which is the part of the URL after team name
            but before & and ?. Includes / if required.
        """
        # remove file extension
        upload_path = self.path.parent / self.path.stem
        # add 'CSS'
        upload_path = str(upload_path) + 'CSS'

        return "/" + upload_path

    def _generate_upload_URL(self):
        """
            Returns the URL of the iGEM page where this file can be uploaded.
            Private function. Use upload_URL to access instead.
        """

        return 'https://2020.igem.org/wiki/index.php?title=Template:' + self._config['team'] + \
            self._upload_path + '&action=edit'

    def _generate_link_URL(self):
        """
            Returns the iGEM URL where this page will be found and can be linked to.
        """
        return 'https://2020.igem.org/Template:' + self._config['team'] + \
            self._upload_path + '?action=raw&ctype=text/css'


class JSfile(BaseFile):
    def __init__(self, path, config):
        BaseFile.__init__(self, path, config)
        self._upload_path = self._generate_upload_path()
        self._upload_URL = self._generate_upload_URL()
        self._link_URL = self._generate_link_URL()

    @property
    def upload_URL(self):
        return self._upload_URL

    @property
    def link_URL(self):
        return self._link_URL

    def _generate_upload_path(self):
        """
            Returns upload path, which is the part of the URL after team name
            but before & and all. Includes / if required.
        """
        # remove file extension
        upload_path = self.path.parent / self.path.stem
        # add 'CSS'
        upload_path = str(upload_path) + 'JS'

        return "/" + upload_path

    def _generate_upload_URL(self):
        """
            Returns the URL of the iGEM page where this file can be uploaded.
            Private function. Use upload_URL to access instead.
        """
        return 'https://2020.igem.org/wiki/index.php?title=Template:' + self._config['team'] + \
            self._upload_path + '&action=edit'

    def _generate_link_URL(self):
        """
            Returns the iGEM URL where this page will be found and can be linked to.
        """
        return 'https://2020.igem.org/Template:' + self._config['team'] + \
            self._upload_path + '?action=raw&ctype=text/javascript'


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
    absoluteSourceDir = Path('.').resolve() / src_dir

    def replacer(url):
        p = Path(url)

        absoluteLocalURL = (os.path.dirname(cssFilePath) / p).resolve()
        relativeToSourceDir = absoluteLocalURL.relative_to(absoluteSourceDir)

        return str(relativeToSourceDir)

    cssutils.replaceUrls(sheet, replacer=replacer)
    contents = sheet.cssText.decode("utf-8")
    return contents


def JShandler(team, contents):

    contents = jsmin(contents)
    return contents
