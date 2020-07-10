from datetime import datetime
from bs4 import BeautifulSoup

def iGEM_login(browser, credentials):

    browser.open("https://igem.org/Login2")
    browser.select_form('form[method="post"]')
    browser["username"] = credentials['username']
    browser["password"] = credentials['password']
    response = browser.submit_selected()

    soup = BeautifulSoup(response.text, 'html5lib')
    # TODO: Add error handling
    return soup.text

def iGEM_upload_page(browser, credentials, contents, url):

    # TODO: Think about a way to do this without passing credentials.
    
    # except runs if try fails
    # else runs if try succeeds
    for attempt in range(3):
        try:
            browser.open(url)
        except:
            iGEM_login(browser, credentials)
        else:
            break
            # TODO: Add error handling
    
    browser.select_form('form')
    browser['wpTextbox1'] = contents
    response = browser.submit_selected()
    # TODO: Add error handling

    print('Uploaded to', url)

    return response.text

def iGEM_upload_file(browser, credentials, file_object):

    # TODO: Think about a way to do this without passing credentials.

    url = file_object.upload_URL
    # except runs if try fails
    # else runs if try succeeds
    for attempt in range(3):
        try:
            browser.open(url)
        except ConnectionError:
            iGEM_login(browser, credentials)
        else:
            break
        # TODO: Add error handling

    
    browser.select_form('form')
    browser['wpUploadFile'] = str(file_object.src_path)
    browser['wpDestFile'] = file_object.upload_filename
    # browser['wpUploadDescription'] = 'BITSPilani-Goa_India team logo'
    browser['wpIgnoreWarning'] = "1"
    response = browser.submit_selected()
    # TODO: Add error handling

    relative_link = browser.get_current_page().find(class_='fullMedia').find('a')['href']
    file_object.set_upload_URL('https://2020.igem.org' + relative_link)

    print('Uploaded', file_object.upload_filename, 'to', file_object.upload_URL)
    
    return response

