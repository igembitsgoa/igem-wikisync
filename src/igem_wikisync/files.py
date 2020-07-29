import hashlib
from pathlib import Path


class BaseFile:
    '''Base class for all file objects. Not to be used directly.
    Use HTMLfile, CSSfile, JSfile or OtherFile instead.
    '''

    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.

    def __init__(self, path, config):
        self._config = config

        self._path = Path(path)

        self._stem = str(self._path.stem)
        self._extension = str(self._path.suffix[1:]).lower()
        self._filename = str(self._stem + '.' + self._extension)
        self._parent = self._path.parent
        self._src_path = self._config['src_dir'] / self._path
        self._build_path = self._config['build_dir'] / self._path
        self._upload_URL = None  # URL of the upload form for file
        self._link_URL = None   # URL where the file will live

    @property
    def path(self):
        ''' Path of the file relative to src_dir. '''
        return self._path

    @property
    def filename(self):
        ''' Filename with extension. '''
        return self._filename

    @property
    def extension(self):
        ''' File extension. '''
        return self._extension

    # @property
    # def parent(self):
    #     ''' Path without the filename and terminal /. '''
    #     return self._parent

    @property
    def src_path(self):
        ''' Build path with src_dir. (src_dir/..)'''
        return self._src_path

    @property
    def build_path(self):
        ''' Build path with build_dir (build_dir/..). '''
        return self._build_path

    @property
    def upload_URL(self):
        ''' URL of the upload form for this file. '''
        return self._upload_URL

    @property
    def link_URL(self):
        ''' URL which can be used to link to this file. '''
        return self._link_URL

    @property
    def raw_URL(self):
        ''' URL where raw content can be found.
        Same as link_URL for JS and CSS.
        For HTML files, raw page content will be found,
        without wrapper iGEM HTML.
        '''
        return self._raw_URL


class HTMLfile(BaseFile):
    '''
    Container class that derives file properties for later use.
    :param path: File path relative to the current directory.
    :type path: str or :class:`pathlib.Path`
    '''

    def __init__(self, path, config):
        BaseFile.__init__(self, path, config)
        self._upload_path = self._generate_upload_path()
        self._upload_URL = self._generate_upload_URL()
        self._link_URL = self._generate_link_URL()
        self._raw_URL = self._generate_raw_URL()

    def _generate_upload_path(self):
        '''
            Returns upload path, which is the part of the URL after team name
            but before & and all. Includes / if required.
        '''

        # remove /index.html
        if 'index.html' in str(self.path):
            upload_path = str(self.path.parent)
        else:
            upload_path = str(self.path.parent / self.path.stem)

        if upload_path == '.':
            return ''
        else:
            return '/' + upload_path

    def _generate_upload_URL(self):
        '''
            Returns the URL of the iGEM page where this file can be uploaded.
            Private function. Use upload_URL to access instead.
        '''
        return 'https://' + self._config['year'] + '.igem.org/wiki/index.php?title=Team:' + \
            self._config['team'] + self._upload_path + '&action=edit'

    def _generate_link_URL(self):
        '''
            Returns the iGEM URL where this page will be found and can be linked to.
            Private function. Use link_URL to access instead.
        '''
        return 'https://' + self._config['year'] + '.igem.org/Team:' + self._config['team'] + \
            self._upload_path

    def _generate_raw_URL(self):
        '''
            Returns the iGEM URL where this page will be found and can be linked to.
            Private function. Use link_URL to access instead.
        '''
        return 'https://' + self._config['year'] + '.igem.org/wiki/index.php?title=Team:' + \
            self._config['team'] + self._upload_path + '&action=raw'


class CSSfile(BaseFile):
    def __init__(self, path, config):
        BaseFile.__init__(self, path, config)
        self._upload_path = self._generate_upload_path()
        self._upload_URL = self._generate_upload_URL()
        self._link_URL = self._generate_link_URL()
        self._raw_URL = self._link_URL

    def _generate_upload_path(self):
        '''
            Returns upload path, which is the part of the URL after team name
            but before & and ?. Includes / if required.
        '''
        # remove file extension
        upload_path = self.path.parent / self.path.stem
        # add 'CSS'
        upload_path = str(upload_path).replace('.', '-') + 'CSS'

        return '/' + upload_path

    def _generate_upload_URL(self):
        '''
            Returns the URL of the iGEM page where this file can be uploaded.
            Private function. Use upload_URL to access instead.
        '''

        return 'https://' + self._config['year'] + '.igem.org/wiki/index.php?title=Template:' + self._config['team'] + \
            self._upload_path + '&action=edit'

    def _generate_link_URL(self):
        '''
            Returns the iGEM URL where this page will be found and can be linked to.
        '''
        return 'https://' + self._config['year'] + '.igem.org/Template:' + self._config['team'] + \
            self._upload_path + '?action=raw&ctype=text/css'


class JSfile(BaseFile):
    def __init__(self, path, config):
        BaseFile.__init__(self, path, config)
        self._upload_path = self._generate_upload_path()
        self._upload_URL = self._generate_upload_URL()
        self._link_URL = self._generate_link_URL()
        self._raw_URL = self._link_URL

    def _generate_upload_path(self):
        '''
            Returns upload path, which is the part of the URL after team name
            but before & and all. Includes / if required.
        '''
        # remove file extension
        upload_path = self.path.parent / self.path.stem
        # add 'JS'
        upload_path = str(upload_path).replace('.', '-') + 'JS'

        return '/' + upload_path

    def _generate_upload_URL(self):
        '''
            Returns the URL of the iGEM page where this file can be uploaded.
            Private function. Use upload_URL to access instead.
        '''
        return 'https://' + self._config['year'] + '.igem.org/wiki/index.php?title=Template:' + self._config['team'] + \
            self._upload_path + '&action=edit'

    def _generate_link_URL(self):
        '''
            Returns the iGEM URL where this page will be found and can be linked to.
        '''
        return 'https://' + self._config['year'] + '.igem.org/Template:' + self._config['team'] + \
            self._upload_path + '?action=raw&ctype=text/javascript'


class OtherFile(BaseFile):
    def __init__(self, path, config):
        BaseFile.__init__(self, path, config)
        self._upload_URL = 'https://' + self._config['year'] + '.igem.org/Special:Upload'
        self._upload_filename = self._generate_upload_filename()
        self._md5_hash = self._generate_md5_hash()

    @property
    def upload_filename(self):
        ''' Filename on iGEM servers. '''
        return self._upload_filename

    # Only OtherFile objects have this property because
    # md5 hashes of other objects are hashes of the modified
    # content, while OtherFiles don't require any modification.
    # Besides, OtherFile md5_hash is a file hash while other
    # hashes are computed on strings (modified file contents)
    @property
    def md5_hash(self):
        ''' MD5 hash of the file. '''
        return self._md5_hash

    def _generate_upload_filename(self):
        # if len(self._config['assets']) == 1:
        if self.filename[:3] != 'T--':
            return 'T--' + self._config['team'] + '--' + '--'.join(self.path.parts[1:])
        else:
            return self.filename
        # else:
        #   return 'T--' + self._config['team'] + '--' + '--'.join(self.path.parts)

    def _generate_md5_hash(self):
        '''
            Returns the MD5 hash of the file
        '''

        # import os
        # return os.getcwd()

        # make a hash object
        h = hashlib.md5()

        # open file for reading in binary mode
        with open(self.src_path, 'rb') as file:

            # loop till the end of the file
            chunk = 0
            while chunk != b'':
                # read only 1024 bytes at a time
                chunk = file.read(1024)
                h.update(chunk)

        # return the hex representation of digest
        return h.hexdigest()

    def set_link_URL(self, url):
        self._link_URL = url
