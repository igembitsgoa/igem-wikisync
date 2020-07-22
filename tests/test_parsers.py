from igem_wikisync.parsers import HTMLparser, CSSparser, JSparser
import pytest

@pytest.fixture
def config():
    return {
        'team': 'BITSPilani-Goa_India',
        'src_dir': 'tests/src',
        'build_dir': 'tests/build'
    }

def test_HTMLparser(config):
    with open('tests/src/index.html', 'r') as file:
        contents = file.read()

        