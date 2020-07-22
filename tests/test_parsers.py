from igem_wikisync.parsers import HTMLparser, CSSparser, JSparser
import pytest
import hashlib

@pytest.fixture
def config():
    return {
        'team': 'BITSPilani-Goa_India',
        'src_dir': 'tests/src',
        'build_dir': 'tests/build'
    }

@pytest.fixture
def upload_map():
    return {
        'assets': {
            'assets/img/logo.jpg': {
                'link_URL': 'somerandomURLthatiGEMsends'
            }
        }
    }

def test_HTMLparser(config, upload_map):
    with open('tests/src/index.html', 'r') as file:
        contents = file.read()

    parsed = HTMLparser(config, 'index.html', contents, upload_map)

    # assert parsed == 'hello'

    assert hashlib.md5(parsed.encode('UTF-8')).hexdigest() == 'ec80a71cc644c2494d9bdf29681f0386'

def test_JSparser():
    with open('tests/src/index.js', 'r') as file:
        contents = file.read()

    parsed = JSparser(contents)

    # assert parsed == 'hello'

    assert hashlib.md5(parsed.encode('UTF-8')).hexdigest() == '1379876862c68797d5f9ab3edd60a7f9'