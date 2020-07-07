import re
from pathlib import Path
import hashlib


def is_relative(url):
    """ Returns whether given URL is relative. """
    # https://stackoverflow.com/a/31991870/1907830
    return not bool(re.match('(?:^[a-z][a-z0-9+.-]*:|\/\/)', url))


def resolve_relative_URL(config, parent, url):
    """ 
        Resolves a given relative URL to it's absolute counterpart, 
        based on the build_dir and location of the folder where 
        the URL was found.
    """

    build_dir = Path(config['build_dir']).resolve()
    p = (build_dir / parent / url).resolve().relative_to(build_dir)

    return p


def iGEM_URL(config, path):
    """ 
        Replaces a given absolute local URL with it's iGEM counterpart.
    """

    return path

    # if extension == 'CSS':
    #     filetype = 'css'
    # elif extension == 'JS':
    #     filetype = 'javascript'

    # absolute = os.path.splitext(relative)[0] + extension
    # if absolute[0] != '/':
    #     absolute = '/' + absolute
    # absolute = 'https://2020.igem.org/Template:' + team + absolute + '?action=raw&ctype=text/' + filetype

    # return absolute

