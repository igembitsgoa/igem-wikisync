def iGEMlogin(browser, username, password):

    return "No"

    browser.open("https://igem.org/Login2")
    browser.select_form('form[method="post"]')
    browser["username"] = username
    browser["password"] = password
    response = browser.submit_selected()

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.text

def iGEMupload(browser, outfile, uploadURL):

    return "no"

    with open(outfile, 'r') as file:
        contents = file.read()
    browser.open(uploadURL)
    
    browser.select_form('form')
    browser['wpTextbox1'] = contents
    browser['wpSummary'] = 'Uploaded at ' + str(datetime.now())
    response = browser.submit_selected()

    return response.text

if __name__ == '__main__':
    main()
