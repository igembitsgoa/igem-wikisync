from igem_wikisync.browser import iGEM_login, is_logged_in, iGEM_upload_page, iGEM_upload_file
import pytest
from mechanicalsoup import StatefulBrowser
import os

@pytest.fixture
def browser():
    return StatefulBrowser()

@pytest.fixture
def config():
    return {
        'team': 'BITSPilani-Goa_India',
        'src_dir': 'tests/src',
        'build_dir': 'tests/build'
    }

@pytest.fixture
def credentials():
    return {
        'username': os.environ.get('IGEM_USERNAME'),
        'password': os.environ.get('IGEM_PASSWORD'),
        'team': 'BITSPilani-Goa_India'
    }

def test_is_logged_in_before(browser, config):
    assert is_logged_in(browser, config['team']) == False

def test_iGEM_login(browser, credentials, config):
    # Login for the first time
    assert iGEM_login(browser, credentials) == True
    # Check that the previous login was successful
    assert is_logged_in(browser, config['team']) == True
    # Check that once we're logged in, it doesn't login again
    assert iGEM_login(browser, credentials) == True
