import os
import re
from pathlib import Path

from igem_wikisync.files import CSSfile
from igem_wikisync.files import HTMLfile
from igem_wikisync.files import JSfile
from igem_wikisync.logger import logger


def is_relative(url):
    """ Returns whether given URL is relative. """
    # https://stackoverflow.com/a/31991870/1907830
    absolute = bool(re.match(r'(?:^[a-z][a-z0-9+.-]*:|\/\/)', url))
    # absolute = bool(re.match('(?:^[a-z][a-z0-9+.-]*:|\/\/)', url))
    hashtag = url[0] == '#'
    return not absolute and not hashtag


def resolve_relative_URL(config: dict, parent: Path, url: str) -> Path:
    """
        Resolves a given relative URL to it's absolute local counterpart.
        Returned URL is relative to src_dir.
    """

    src_dir = Path(config['src_dir']).resolve()

    # remove trailing /
    if url[-1] == '/':
        url = url[:-1]

    # remove leading /
    if url[0] == '/':
        url = url[1:]
        full_path = (src_dir / url).resolve()
    else:
        full_path = (src_dir / parent / url).resolve()

    if full_path.is_dir() or full_path.suffix == '':
        return (full_path / 'index.html').relative_to(src_dir)
    else:
        return full_path.relative_to(src_dir)


def iGEM_URL(config: dict, path: Path, upload_map: dict, url: str) -> str:
    """
        Replaces a given absolute local URL with it's iGEM counterpart.
    """

    if not is_relative(url):
        return url

    if url == '/':
        return 'https://2020.igem.org/Team:' + config['team']

    old_path = url
    resolved_path = resolve_relative_URL(config, path.parent, url)

    # check upload_map
    found = False
    for filetype in upload_map.keys():
        if str(resolved_path) in upload_map[filetype].keys():
            url = upload_map[filetype][str(resolved_path)]['link_URL']
            found = True
            break

    if not found:
        # check if file exists
        filepath = config['src_dir'] / resolved_path

        if not os.path.isfile(filepath):
            message = f"Warning: {filepath} is referenced in {config['src_dir'] / path} but was not found."
            logger.error(message)

        extension = resolved_path.suffix[1:].lower()

        # create file object
        if extension == 'html':
            file_object = HTMLfile(config['src_dir'] / resolved_path, config)
            url = file_object.link_URL
        elif extension == 'css':
            file_object = CSSfile(config['src_dir'] / resolved_path, config)
            url = file_object.link_URL
        elif extension == 'js':
            file_object = JSfile(config['src_dir'] / resolved_path, config)
            url = file_object.link_URL

    logger.info(f"{old_path} was changed to {url} in {path}.")

    return url
