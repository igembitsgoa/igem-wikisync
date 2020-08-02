from datetime import date

import pytest

from igem_wikisync.files import CSSfile
from igem_wikisync.files import HTMLfile
from igem_wikisync.files import JSfile
from igem_wikisync.files import OtherFile


@pytest.fixture
def config():
    return {
        'team': 'BITSPilani-Goa_India',
        'src_dir': 'tests/data',
        'build_dir': 'tests/build',
        'year': str(date.today().year)
    }


def test_HTMLfile(config):
    html_file = HTMLfile('Test/index.html', config)

    assert str(html_file.path) == 'Test/index.html'
    assert str(html_file.filename) == 'index.html'
    assert str(html_file.extension) == 'html'
    assert str(html_file.src_path) == 'tests/data/Test/index.html'
    assert str(html_file.build_path) == 'tests/build/Test/index.html'
    assert str(html_file.upload_URL) == 'https://2020.igem.org/wiki/index.php?title=Team:BITSPilani-Goa_India/Test&action=edit'
    assert str(html_file.link_URL) == 'https://2020.igem.org/Team:BITSPilani-Goa_India/Test'
    assert str(html_file.raw_URL) == 'https://2020.igem.org/wiki/index.php?title=Team:BITSPilani-Goa_India/Test&action=raw'

    html_file2 = HTMLfile('index.html', config)
    assert str(html_file2.upload_URL) == 'https://2020.igem.org/wiki/index.php?title=Team:BITSPilani-Goa_India&action=edit'


def test_CSSfile(config):
    css_file = CSSfile('Test/css/style.css', config)

    assert str(css_file.path) == 'Test/css/style.css'
    assert str(css_file.filename) == 'style.css'
    assert str(css_file.extension) == 'css'
    assert str(css_file.src_path) == 'tests/data/Test/css/style.css'
    assert str(css_file.build_path) == 'tests/build/Test/css/style.css'
    assert str(css_file.upload_URL) == \
        'https://2020.igem.org/wiki/index.php?title=Template:BITSPilani-Goa_India/Test/css/styleCSS&action=edit'
    assert str(css_file.link_URL) == 'https://2020.igem.org/Template:BITSPilani-Goa_India/Test/css/styleCSS?action=raw&ctype=text/css'
    assert str(css_file.raw_URL) == 'https://2020.igem.org/Template:BITSPilani-Goa_India/Test/css/styleCSS?action=raw&ctype=text/css'


def test_JSfile(config):
    js_file = JSfile('Test/js/index.js', config)

    assert str(js_file.path) == 'Test/js/index.js'
    assert str(js_file.filename) == 'index.js'
    assert str(js_file.extension) == 'js'
    assert str(js_file.src_path) == 'tests/data/Test/js/index.js'
    assert str(js_file.build_path) == 'tests/build/Test/js/index.js'
    assert str(js_file.upload_URL) == 'https://2020.igem.org/wiki/index.php?title=Template:BITSPilani-Goa_India/Test/js/indexJS&action=edit'
    assert str(js_file.link_URL) == 'https://2020.igem.org/Template:BITSPilani-Goa_India/Test/js/indexJS?action=raw&ctype=text/javascript'
    assert str(js_file.raw_URL) == 'https://2020.igem.org/Template:BITSPilani-Goa_India/Test/js/indexJS?action=raw&ctype=text/javascript'


def test_OtherFile(config):
    # OtherFile assumes that the path starts from 'assets'
    other_file = OtherFile('assets/img/test.jpg', config)

    assert str(other_file.path) == 'assets/img/test.jpg'
    assert str(other_file.filename) == 'test.jpg'
    assert str(other_file.extension) == 'jpg'
    assert str(other_file.src_path) == 'tests/data/assets/img/test.jpg'
    assert str(other_file.build_path) == 'tests/build/assets/img/test.jpg'
    assert str(other_file.upload_URL) == 'https://2020.igem.org/Special:Upload'
    assert str(other_file.upload_filename) == 'T--BITSPilani-Goa_India--img--test.jpg'

    assert (str(other_file.md5_hash)) == 'd47d3629a83090c33e94c961e03a03d2'

    url = 'hello'
    other_file.set_link_URL(url)
    assert str(other_file.link_URL) == 'hello'
