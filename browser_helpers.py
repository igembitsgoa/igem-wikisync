from bs4 import BeautifulSoup

def iGEM_login(browser, username, password):

    browser.open("https://igem.org/Login2")
    browser.select_form('form[method="post"]')
    browser["username"] = username
    browser["password"] = password
    response = browser.submit_selected()

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.text

def iGEM_upload_page(browser, path, url):

    return "no"

    with open(path, 'r') as file:
        contents = file.read()
    browser.open(url)
    
    browser.select_form('form')
    browser['wpTextbox1'] = contents
    browser['wpSummary'] = 'Uploaded at ' + str(datetime.now())
    response = browser.submit_selected()

    return response.text

def iGEM_upload_file(browser, file_object):

    url = file_object.upload_URL
    team = file_object.config['team']
    browser.open(url)
    
    browser.select_form('form')
    browser['wpUploadFile'] = str(file_object.src_path)
    browser['wpDestFile'] = 'T--' + team + '--' + file_object.filename
    # browser['wpUploadDescription'] = 'BITSPilani-Goa_India team logo'
    browser['wpIgnoreWarning'] = "1"
    response = browser.submit_selected()
    relative_link = browser.get_current_page().find(class_='fullMedia').find('a')['href']
    file_object.set_upload_URL('https://2020.igem.org' + relative_link)

    print('Uploaded', file_object.upload_filename, 'to', file_object.upload_URL)
    
    return response

