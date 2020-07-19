from datetime import datetime

from bs4 import BeautifulSoup

from igem_wikisync.logger import logger


def iGEM_login(browser, credentials):
    # Raises SystemExit if fails to login.
    # If we want to support building without uploading,
    # this function will never be called.

    if is_logged_in(browser, credentials['team']):
        logger.info(f"Already logged in as {credentials['username']}.")
        return True

    url = "https://igem.org/Login2"

    try:
        response = browser.open(url)
    except Exception:
        message = f"Couldn't connect to {url}."
        logger.debug(message, exc_info=True)
        logger.error(message)
        raise SystemExit

    if response.status_code != 200:
        message = f"Failed to login. {url} was not found."
        logger.debug(message, exc_info=True)
        logger.error(message)
        raise SystemExit

    try:
        browser.select_form('form[method="post"]')
    except Exception:
        message = f"Couldn't find the login form at {url}. " + \
            "Has the login page changed?"
        logger.debug(message, exc_info=True)
        logger.error(message)
        raise SystemExit

    browser["username"] = credentials['username']
    browser["password"] = credentials['password']

    try:
        response = browser.submit_selected()
    except Exception:
        message = "Lost connection to iGEM servers."
        logger.debug(message, exc_info=True)
        logger.error(message)
        raise SystemExit

    soup = BeautifulSoup(response.text, 'html5lib')

    if "successfully logged in" in soup.text:
        logger.info(f"Successfully logged in as {credentials['username']}.")
        return True
    elif "That username is not valid" in soup.text:
        message = "Your iGEM username is invalid."
        logger.error(message)
    elif "That username is valid, but the password is not" in soup.text:
        message = "Your iGEM username is valid but the password is not."
        logger.error(message)
    else:
        message = "An unknown error occured while trying to login."
        logger.error(message)

    raise SystemExit


def is_logged_in(browser, team):

    url = 'https://2020.igem.org/Team:' + team + \
        '/' + str(datetime.now().microsecond ** 2)

    try:
        browser.open(url)
    except Exception:
        message = "Couldn't connect to iGEM. Please check your internet connection."
        logger.debug(message, exc_info=True)
        logger.error(message)
        raise SystemExit

    soup = browser.get_current_page()

    message = soup.text

    if "do not have permission" in message:
        return False
    elif "edit this page" in message:
        return True

    return False


def iGEM_upload_page(browser, contents, url):

    # except runs if try fails
    # else runs if try succeeds
    browser.open(url)  # TODO: Check this

    try:
        browser.select_form('form')
    except Exception:
        message = f"Couldn't find the form at {url}. Has the page changed?"
        logger.debug(message, exc_info=True)
        logger.error(message)
        raise SystemExit

    browser['wpTextbox1'] = contents
    try:
        response = browser.submit_selected()
    except Exception:
        message = f"Couldn't upload to {url}."
        logger.debug(message, exc_info=True)
        logger.error(message)
        raise SystemExit

    logger.info(f'Uploaded to {url}.')

    return response.text


def iGEM_upload_file(browser, credentials, file_object):

    url = file_object.upload_URL
    browser.open(url)  # TODO: Check this

    try:
        browser.select_form('form')
    except Exception:
        message = f"Couldn't find the form at {url}. Has the page changed?"
        logger.debug(message, exc_info=True)
        logger.error(message)
        raise SystemExit

    browser['wpUploadFile'] = str(file_object.src_path)
    browser['wpDestFile'] = file_object.upload_filename

    # * Ignore all warnings
    # We keep track of already uploaded files internally
    browser['wpIgnoreWarning'] = "1"

    try:
        response = browser.submit_selected()
    except Exception:
        message = "Lost connection to iGEM servers."
        logger.debug(message, exc_info=True)
        logger.error(message)
        raise

    relative_link = browser.get_current_page().find(
        class_='fullMedia').find('a')['href']
    file_object.set_upload_URL('https://2020.igem.org' + relative_link)

    logger.info(f'Uploaded {file_object.upload_filename} to {file_object.upload_URL}.')

    return response
