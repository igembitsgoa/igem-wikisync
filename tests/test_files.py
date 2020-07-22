from igem_wikisync.files import HTMLfile, CSSfile, JSfile, OtherFile
import pytest

@pytest.fixture
def config():
    return {
        'team': 'BITSPilani-Goa_India',
        'src_dir': 'tests/src',
        'build_dir': 'tests/build'
    }

def test_HTMLfile(config):
    html_file = HTMLfile('tests/src/index.html', config)

    assert str(html_file.path) == 'index.html'
    assert str(html_file.filename) == 'index.html'
    assert str(html_file.extension) == 'html'
    assert str(html_file.src_path) == 'tests/src/index.html'
    assert str(html_file.build_path) == 'tests/build/index.html'
    assert str(html_file.upload_URL) == 'https://2020.igem.org/wiki/index.php?title=Team:BITSPilani-Goa_India&action=edit'
    assert str(html_file.link_URL) == 'https://2020.igem.org/Team:BITSPilani-Goa_India'

def test_CSSfile(config):
    css_file = CSSfile('tests/src/css/style.css', config)

    assert str(css_file.path) == 'css/style.css'
    assert str(css_file.filename) == 'style.css'
    assert str(css_file.extension) == 'css'
    assert str(css_file.src_path) == 'tests/src/css/style.css'
    assert str(css_file.build_path) == 'tests/build/css/style.css'
    assert str(css_file.upload_URL) == 'https://2020.igem.org/wiki/index.php?title=Template:BITSPilani-Goa_India/css/styleCSS&action=edit'
    assert str(css_file.link_URL) == 'https://2020.igem.org/Template:BITSPilani-Goa_India/css/styleCSS?action=raw&ctype=text/css'

def test_JSfile(config):
    js_file = JSfile('tests/src/js/index.js', config)

    assert str(js_file.path) == 'js/index.js'
    assert str(js_file.filename) == 'index.js'
    assert str(js_file.extension) == 'js'
    assert str(js_file.src_path) == 'tests/src/js/index.js'
    assert str(js_file.build_path) == 'tests/build/js/index.js'
    assert str(js_file.upload_URL) == 'https://2020.igem.org/wiki/index.php?title=Template:BITSPilani-Goa_India/js/indexJS&action=edit'
    assert str(js_file.link_URL) == 'https://2020.igem.org/Template:BITSPilani-Goa_India/js/indexJS?action=raw&ctype=text/javascript'

def test_OtherFile(config):
    other_file = OtherFile('tests/src/assets/img/logo.jpg', config)

    assert str(other_file.path) == 'assets/img/logo.jpg'
    assert str(other_file.filename) == 'logo.jpg'
    assert str(other_file.extension) == 'jpg'
    assert str(other_file.src_path) == 'tests/src/assets/img/logo.jpg'
    assert str(other_file.build_path) == 'tests/build/assets/img/logo.jpg'
    assert str(other_file.upload_URL) == 'https://2020.igem.org/Special:Upload'
    assert str(other_file.upload_filename) == 'T--BITSPilani-Goa_India--img--logo.jpg'

    assert (str(other_file.md5_hash)) == '1f43f07ffb7056e484f523846e8e198d35571235'

    url = 'hello'
    other_file.set_upload_URL(url)
    assert str(other_file.upload_URL) == 'hello'

