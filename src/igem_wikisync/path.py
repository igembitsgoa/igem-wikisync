import os
import re
from pathlib import Path

from igem_wikisync.files import CSSfile
from igem_wikisync.files import HTMLfile
from igem_wikisync.files import JSfile
from igem_wikisync.logger import logger


def is_relative(url: str) -> bool:
    """ Returns whether given URL is relative. """
    # https://stackoverflow.com/a/31991870/1907830
    absolute = bool(re.match(r'(?:^[a-z][a-z0-9+.-]*:|\/\/)', url))
    # absolute = bool(re.match('(?:^[a-z][a-z0-9+.-]*:|\/\/)', url))
    hashtag = url[0] == '#'
    return not absolute and not hashtag


def resolve_relative_path(path: str, parent: Path, src_dir: str) -> Path:
    """
    Resolves a given relative path to it's absolute local counterpart.
    Assumes that the passed path is relative.
    Returned path is relative to src_dir.

    Arguments:
        path:    path to be resolved.
        parent: Path to the folder where the passed in path was found.
            This can be relative to the directory where the function
            call originates, or an absolute path.
        src_dir: Directory where all input files are stored.

    Returns:
        Resolved path, relative to src_dir.
    """

    # TODO: Understand and comment this function.

    src_dir = Path(src_dir).resolve()

    # remove trailing /
    if path[-1] == '/':
        path = path[:-1]

    # remove leading /
    if path[0] == '/':
        path = path[1:]
        full_path = (src_dir / path).resolve()
    else:
        full_path = (src_dir / parent / path).resolve()

    if full_path.is_dir() or full_path.suffix == '':
        return (full_path / 'index.html').relative_to(src_dir)
    else:
        return full_path.relative_to(src_dir)


def iGEM_URL(config: dict, path: Path, upload_map: dict, url: str) -> str:
    """
    Replaces a given absolute local URL with it's iGEM counterpart.

    Arguments:
        config: Dictionary containing 'src_dir', 'team' and 'build_dir'.
        path: path to the file where this URL was found
        upload_map: custom upload map
        url: the absolute path to be converted

    Returns:
        URL where this file would be found on iGEM servers.
        Returns false if URL with an unsupported extension is passed
    """

    if config['silence_warnings']:
        logger.handlers[0].setLevel(40)

    # Store input for logging and/or returning
    old_path = url

    # Convert to path in case a string was passed
    path = Path(path)

    # return if it's already absolute
    if not is_relative(url):
        return url

    if url == '/':
        return 'https://' + config['year'] + '.igem.org/Team:' + config['team']

    # Resolve relative path to local absolute path
    resolved_path = resolve_relative_path(url, path.parent, config['src_dir'])

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
            message = f"{filepath} is referenced in {config['src_dir'] / path} but was not found."
            logger.warning(message)

        extension = resolved_path.suffix[1:].lower()

        # create imaginary file object and
        # let the functions in that class handle creating URLs
        if extension == 'html':
            file_object = HTMLfile(resolved_path, config)
            url = file_object.link_URL
        elif extension == 'css':
            file_object = CSSfile(resolved_path, config)
            url = file_object.link_URL
        elif extension == 'js':
            file_object = JSfile(resolved_path, config)
            url = file_object.link_URL
        # leave unchanged
        else:
            logger.warning(f"{old_path} is referenced in {path} but was not found.")
            return old_path

    logger.info(f"{old_path} was changed to {url} in {path}.")
    return url
