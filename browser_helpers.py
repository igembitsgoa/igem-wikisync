from datetime import datetime
from bs4 import BeautifulSoup

def iGEM_login(browser, credentials):
    # Raises SystemExit if fails to login.
    # If we want to support building without uploading, 
    # this function will never be called.

    url = "https://igem.org/Login2"

    try:
        response = browser.open(url)
    except Exception as error:
        print("Couldn't connect to", url, ".")
        print(error)
        raise SystemExit
        
    if response.status_code != 200:
        print("Failed to login.", url, "was not found.")
        raise SystemExit

    try:
        browser.select_form('form[method="post"]')
    except:
        print("Couldn't find the login form at " + url + ". Has the login page changed?")
        raise SystemExit

    browser["username"] = credentials['username']
    browser["password"] = credentials['password']

    try:
        response = browser.submit_selected()
    except Exception as error:
        print("Lost connection to iGEM servers.")
        print(error)
        raise SystemExit

    soup = BeautifulSoup(response.text, 'html5lib')

    if "successfully logged in" in soup.text:
        return True
    elif "That username is not valid" in soup.text:
        print("Your iGEM username is invalid.")
    elif "That username is valid, but the password is not" in soup.text:
        print("Your iGEM username is valid but the password is not.")
    else:
        print("An unknown error occured while trying to login.")

    raise SystemExit

def iGEM_upload_page(browser, credentials, contents, url, attempts=3):

    # TODO: Think about a way to do this without passing credentials.
    
    # except runs if try fails
    # else runs if try succeeds
    try:
        browser.open(url)
    except:
        raise ConnectionError
    
    try:
        browser.select_form('form')
    except:
        print("Couldn't find the form at", url + ". Has the page changed?")
        raise SystemExit

    browser['wpTextbox1'] = contents
    try:
        response = browser.submit_selected()
    except Exception as error:
        print("Couldn't upload to", url)
        print(error)
        raise SystemExit

    print('Uploaded to', url)

    return response.text

def iGEM_upload_file(browser, credentials, file_object, attempts=3):

    # TODO: Think about a way to do this without passing credentials.

    url = file_object.upload_URL
    try:
        browser.open(url)
    except:
        raise ConnectionError
    
    try:
        browser.select_form('form')
    except:
        print("Couldn't find the form at", url + ". Has the page changed?")
        raise SystemExit

    browser['wpUploadFile'] = str(file_object.src_path)
    browser['wpDestFile'] = file_object.upload_filename

    #* Ignore all warnings
    # We keep track of already uploaded files internally
    browser['wpIgnoreWarning'] = "1"

    try:
        response = browser.submit_selected()
    except FileNotFoundError as error:
        print(file_object.path, "not found. Was it modified during the execution of this program?")
        print(error)
        raise
    except Exception as error:
        print("Lost connection to iGEM servers.")
        print(error)
        raise SystemExit

    relative_link = browser.get_current_page().find(class_='fullMedia').find('a')['href']
    file_object.set_upload_URL('https://2020.igem.org' + relative_link)

    print('Uploaded', file_object.upload_filename, 'to', file_object.upload_URL)
    
    return response

