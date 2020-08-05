from datetime import datetime

from bs4 import BeautifulSoup

from igem_wikisync.logger import logger


def iGEM_login(browser, credentials: dict, config: dict) -> bool:
    """
    Logs into the iGEM server.

    Arguments:
        browser: mechanicalsoup.Browser instance
        credentials: dictionary containing 'username'
            and 'password'
        config: custom configuration dictionary

    Returns:
        True if login is successful.
        False along with an error message otherwise.
    """

    # Check if we're already logged in
    if check_login(browser, config['team'], config['year']):
        logger.info("Already logged in.")
        return True

    # Try opening the login page
    url = "https://igem.org/Login2"
    try:
        response = browser.open(url)
    except Exception:
        message = f"Couldn't connect to {url}."
        logger.debug(message, exc_info=True)
        logger.critical(message)
        return False

    # Check if login was successful
    if response.status_code != 200:
        message = f"Failed to login. {url} was not found."
        logger.debug(message, exc_info=True)
        logger.error(message)
        return False

    # Select the form we have to fill.
    # This might fail if the page changes.
    try:
        browser.select_form('form[method="post"]')
    except Exception:
        message = f"Couldn't find the login form at {url}. " + \
            "Has the login page changed?"
        logger.debug(message, exc_info=True)
        logger.error(message)
        return False

    # Fill the form
    browser["username"] = credentials['username']
    browser["password"] = credentials['password']

    # Try submitting the form
    try:
        response = browser.submit_selected()
    except Exception:
        message = "Lost connection to iGEM servers."
        logger.debug(message, exc_info=True)
        logger.error(message)
        return False

    soup = BeautifulSoup(response.text, 'html5lib')

    # Successful
    if "successfully logged in" in soup.text:
        logger.info(f"Successfully logged in as {credentials['username']}.")
        return True
    # Invalid username
    elif "That username is not valid" in soup.text:
        message = "This iGEM username is invalid."
        logger.error(message)
    # Invalid password
    elif "That username is valid, but the password is not" in soup.text:
        message = "This iGEM username is valid but the password is not."
        logger.error(message)
    # Unknown error
    else:
        message = "An unknown error occured while trying to login."
        logger.error(message)

    return False


def check_login(browser, team: str, year: str) -> bool:
    """
    Check if we're logged into iGEM websites.
    Opens a random iGEM page and checks for edit access.

    Arguments:
        browser: mechanicalsoup.Browser instance
        config: custom config dictionary

    Returns:
        True if we're logged in.
        False otherwise.
    """

    # Try opening a random page within the team
    url = 'https://' + year + '.igem.org/Team:' + team + \
        '/' + str(datetime.now().microsecond ** 2)
    try:
        browser.open(url)
    except Exception:
        message = "Couldn't connect to iGEM. Please check your internet connection."
        logger.debug(message, exc_info=True)
        logger.critical(message)
        return False

    soup = browser.get_current_page()

    message = soup.text

    # Check if we have edit access
    if "do not have permission" in message:
        return False
    elif "edit this page" in message:
        return True

    return False


def iGEM_upload_page(browser, contents: str, url: str) -> bool:
    """
    Uploads source code to the iGEM server.

    Parameters:
        browser: mechanicalsoup.Browser instance
        contents: source code to be uploaded
        url: the page where source code will uploaded

    Returns:
        True if successful, False otherwise.
    """

    # Try opening the iGEM upload page
    try:
        browser.open(url)  # TODO: Check this
    except Exception:
        message = "Lost connection to iGEM. Please check your internet connection."
        logger.debug(message, exc_info=True)
        logger.error(message)
        return False

    # Select the form where source code has to be submitted.
    # This might fail if the source code of the page changes.
    try:
        browser.select_form('form')
    except Exception:
        message = f"Couldn't find the form at {url}. Has the page changed?"
        logger.debug(message, exc_info=True)
        logger.error(message)
        return False

    # Submit the form
    browser['wpTextbox1'] = contents
    try:
        browser.submit_selected()
    except Exception:
        message = f"Couldn't upload to {url}."
        logger.debug(message, exc_info=True)
        logger.error(message)
        return False

    logger.info(f'Uploaded to {url}.')

    return True


def iGEM_upload_file(browser, file_object, year):
    """
    Upload a file to iGEM servers.
    iGEM allows files only 100MB large.
    That check is performed in wikisync.run(), not here.

    Parameters:
        browser: mechanicalsoup.Browser instance
        file_object: igem_wikisync.files.OtherFile object

    Returns:
        True if uploaded, False otherwise.
    """

    # Try opening the iGEM upload page
    url = file_object.upload_URL
    try:
        browser.open(url)  # TODO: Check this
    except Exception:
        message = "Lost connection to iGEM. Please check your internet connection."
        logger.debug(message, exc_info=True)
        logger.error(message)
        return False

    # Select the form where the file has to be uploaded.
    # This might fail if the page changes.
    try:
        browser.select_form('form')
    except Exception:
        message = f"Couldn't find the form at {url}. Has the page changed?"
        logger.debug(message, exc_info=True)
        logger.error(message)
        return False

    browser['wpUploadFile'] = str(file_object.src_path)
    browser['wpUploadDescription'] = 'Uploaded using WikiSync'
    browser['wpDestFile'] = file_object.upload_filename

    # * Ignore all warnings
    # We keep track of already uploaded files internally
    browser['wpIgnoreWarning'] = "1"

    # Submit the form
    try:
        browser.submit_selected()
    except Exception:
        message = "Lost connection to iGEM servers."
        logger.debug(message, exc_info=True)
        logger.error(message)
        return False

    # Extract relative link from response
    relative_link = browser.get_current_page().find(
        class_='fullMedia').find('a')['href']
    file_object.set_link_URL('https://' + year + '.igem.org' + relative_link)

    logger.info(f'Uploaded {file_object.upload_filename} to {file_object.link_URL}.')

    return True
