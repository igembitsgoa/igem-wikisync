import hashlib
from datetime import date

import pytest

from igem_wikisync.parsers import CSSparser, HTMLparser, JSparser


@pytest.fixture
def config():
    return {
        'team': 'BITSPilani-Goa_India',
        'src_dir': 'tests/data',
        'build_dir': 'tests/build',
        'year': str(date.today().year),
        'silence_warnings': False
    }


def md5hash(text):
    return hashlib.md5(text.encode('UTF-8')).hexdigest()


@pytest.fixture
def upload_map():
    return {
        'assets': {
            'assets/img/test.jpg': {
                'link_URL': 'somerandomURLthatiGEMsends'
            },
            'assets/img/test-test.jpg': {
                'link_URL': 'anotherrandomURLthatiGEMsends'
            }
        }
    }


def test_HTMLparser(config, upload_map):
    with open('tests/data/Test/index.html', 'r') as file:
        contents = file.read()

    parsed = HTMLparser(config, 'Test/index.html', contents, upload_map)

    assert md5hash(parsed) == '3efd614407d7bfac36b2832ea47d2512'


def test_HTMLparser_link(config, upload_map):
    with open('tests/data/Test/html/link.html', 'r') as file:
        contents = file.read()
    parsed = HTMLparser(config, 'index.html', contents, upload_map)
    assert md5hash(parsed) == '25ec984a0e9889dab0a0986b1eacee09'


def test_HTMLparser_script(config, upload_map):
    with open('tests/data/Test/html/script.html', 'r') as file:
        contents = file.read()
    parsed = HTMLparser(config, 'index.html', contents, upload_map)
    assert md5hash(parsed) == '727d10aa1f48361ff0fb5236becc3f63'


def test_HTMLparser_internal_styles(config, upload_map):
    with open('tests/data/Test/html/internal-styles.html', 'r') as file:
        contents = file.read()
    parsed = HTMLparser(config, 'Test/html/internal-styles.html', contents, upload_map)
    assert md5hash(parsed) == 'f1bf98174c3a74ceb670af98514f069f'


def test_HTMLparser_img(config, upload_map):
    with open('tests/data/Test/html/img.html', 'r') as file:
        contents = file.read()
    parsed = HTMLparser(config, 'Test/html/img.html', contents, upload_map)
    assert md5hash(parsed) == 'ba2d3f459a58bb24113e481a169016b4'


def test_HTMLparser_srcset1(config, upload_map):
    with open('tests/data/Test/html/srcset1.html', 'r') as file:
        contents = file.read()
    parsed = HTMLparser(config, 'Test/html/srcset1.html', contents, upload_map)
    print(parsed)
    assert md5hash(parsed) == '44dc59824574b54e8f5894f2978fab22'


def test_HTMLparser_srcset2(config, upload_map):
    with open('tests/data/Test/html/srcset2.html', 'r') as file:
        contents = file.read()
    parsed = HTMLparser(config, 'Test/html/srcset2.html', contents, upload_map)
    print(parsed)
    assert md5hash(parsed) == '767a59b62c5b661d3d0c997b314b83de'


def test_HTMLparser_srcset3(config, upload_map):
    with open('tests/data/Test/html/srcset3.html', 'r') as file:
        contents = file.read()
    parsed = HTMLparser(config, 'Test/html/srcset3.html', contents, upload_map)
    print(parsed)
    assert md5hash(parsed) == '644159856c926d23d6f137ee92a694a3'


def test_CSSparser_without_quotes(config, upload_map):
    with open('tests/data/Test/css/without_quotes.css', 'r') as file:
        contents = file.read()

    parsed = CSSparser(config, 'Test/css/without_quotes.css', contents, upload_map)
    assert md5hash(parsed) == 'dcef7d4a8f51008157a019f3e65c10cc'


def test_CSSparser_single_quotes(config, upload_map):
    with open('tests/data/Test/css/single_quotes.css', 'r') as file:
        contents = file.read()

    parsed = CSSparser(config, 'Test/css/style.css', contents, upload_map)

    # assert parsed == 'hello'
    assert md5hash(parsed) == '3f01c1910d12a07e541ae56cd1c3fb35'


def test_CSSparser_double_quotes(config, upload_map):
    with open('tests/data/Test/css/double_quotes.css', 'r') as file:
        contents = file.read()

    parsed = CSSparser(config, 'Test/css/style.css', contents, upload_map)
    assert md5hash(parsed) == 'a2aefc22412100e5b27e34028985a215'


def test_CSSparser_hyphen(config, upload_map):
    with open('tests/data/Test/css/hyphen.css', 'r') as file:
        contents = file.read()

    parsed = CSSparser(config, 'Test/css/style.css', contents, upload_map)
    assert md5hash(parsed) == 'c1aa579595355b4cab71fbb5009f8ca2'


def test_JSparser():
    with open('tests/data/Test/js/index.js', 'r') as file:
        contents = file.read()

    parsed = JSparser(contents)

    assert md5hash(parsed) == '98ceab3bcb66cfe2bc3c07a2bfd56503'
