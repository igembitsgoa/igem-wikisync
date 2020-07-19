from igem_wikisync.files import HTMLfile, CSSfile, JSfile, OtherFile
import pytest

@pytest.fixture
def config():
    return {
        'team': 'BITSPilani-Goa_India',
        'src_dir': 'src',
        'build_dir': 'build'
    }

def test_HTMLfile(config):
    html_file = HTMLfile('src/index.html', config)

    assert str(html_file.path) == 'index.html'
    assert str(html_file.filename) == 'index.html'
    assert str(html_file.extension) == 'html'
    assert str(html_file.src_path) == 'src/index.html'
    assert str(html_file.build_path) == 'build/index.html'
    assert str(html_file.upload_URL) == 'https://2020.igem.org/wiki/index.php?title=Team:BITSPilani-Goa_India&action=edit'
    assert str(html_file.link_URL) == 'https://2020.igem.org/Team:BITSPilani-Goa_India'

