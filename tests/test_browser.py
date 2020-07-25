import os

import mechanicalsoup
import pytest
import requests
import random
import string
from mechanicalsoup import StatefulBrowser
import hashlib

from igem_wikisync.browser import iGEM_login, is_logged_in, iGEM_upload_page, iGEM_upload_file
from igem_wikisync.files import HTMLfile, OtherFile

# I know this is bad
# but I couldn't find a better way to
# maintain the session across tests.
# Please submit a PR if you can improve.
pytest.browser = StatefulBrowser()


@pytest.fixture
def config():
    return {
        'team': 'BITSPilani-Goa_India',
        'src_dir': 'tests/data',
        'build_dir': 'tests/build'
    }


@pytest.fixture
def credentials():
    return {
        'username': os.environ.get('IGEM_USERNAME'),
        'password': os.environ.get('IGEM_PASSWORD'),
        'team': 'BITSPilani-Goa_India'
    }


def md5hash_string(text):
    return hashlib.md5(text.encode('UTF-8')).hexdigest()


def md5hash_file(url):
    ''' Returns the md5 hash of a file from its URL. '''
    r = requests.get(url)

    # make a hash object
    h = hashlib.md5()

    for data in r.iter_content(1024):
        h.update(data)

    return h.hexdigest()


def test_is_logged_in_before(config):
    assert not is_logged_in(pytest.browser, config['team'])


def test_credentials(credentials):
    assert credentials['username'] is not None


def test_iGEM_login(credentials, caplog):
    # Login for the first time
    assert iGEM_login(pytest.browser, credentials)
    assert 'Successfully logged in' in caplog.text


def test_is_logged_in_after(credentials, caplog):
    # Check that once we're logged in, it doesn't login again
    assert iGEM_login(pytest.browser, credentials)
    assert 'Already logged in' in caplog.text


def test_iGEM_upload_page(config, caplog):
    # Read file
    with open('tests/data/Test/html/raw.html') as file:
        contents = file.read()

    # Add a random string
    # to check that the modified data is uploaded everytime
    contents += '\nRandom string for confirmation: '
    contents += ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    # Generate URL
    html_file = HTMLfile('Test/html/raw.html', config)
    url = html_file.upload_URL
    raw_URL = html_file.raw_URL
    print(raw_URL)

    # Upload contents
    assert iGEM_upload_page(pytest.browser, contents, url)

    response = requests.get(raw_URL)
    assert md5hash_string(contents) == md5hash_string(response.text)


def test_iGEM_upload_file(config):
    file_object = OtherFile('assets/img/test.jpg', config)

    iGEM_upload_file(pytest.browser, file_object)

    url = "https://2020.igem.org/wiki/images/5/57/T--BITSPilani-Goa_India--img--test.jpg"

    assert file_object.md5_hash == md5hash_file(url)


def test_iGEM_login_invalid_username(credentials, caplog):
    credentials['username'] = 'helloinvalidusername'

    browser = mechanicalsoup.StatefulBrowser()
    assert not iGEM_login(browser, credentials)
    assert 'username is invalid' in caplog.text


def test_iGEM_login_invalid_password(credentials, caplog):
    credentials['password'] = 'incorrect_password'

    browser = mechanicalsoup.StatefulBrowser()
    assert not iGEM_login(browser, credentials)
    assert 'the password is not' in caplog.text
