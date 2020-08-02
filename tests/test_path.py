from datetime import date

from igem_wikisync.path import iGEM_URL
from igem_wikisync.path import is_relative
from igem_wikisync.path import resolve_relative_path


def test_is_relative():

    absolute_URLs = [
        'https://google.com',
        'https://www.google.com',
        'https://ftp.hello-ftp.google.com',
        'http://google.com',
        'http://www.google.com',
        'http://ftp.helloftp.google.com',
        'ftp://ftp.google.com',
        'mailto:hereisanemail@google.com'
    ]

    for url in absolute_URLs:
        assert not is_relative(url)

    relative_URLs = [
        'index.html',
        'google/index.html',
        '../hello/he-llo',
        '../../hello.html',
        'google/../hello.jpg'
    ]

    for url in relative_URLs:
        assert is_relative(url)


def test_resolve_relative_path():

    assert str(resolve_relative_path('style.css', '.', 'src')) == 'style.css'
    assert str(resolve_relative_path('js/index.js', '.', 'src')) == 'js/index.js'
    assert str(resolve_relative_path('../assets/img/logo.jpg', 'css', 'src')) == 'assets/img/logo.jpg'

    assert str(resolve_relative_path('Description/', '.', 'src')) == 'Description/index.html'
    assert str(resolve_relative_path('/Description', '.', 'src')) == 'Description/index.html'
    assert str(resolve_relative_path('/Description/', '.', 'src')) == 'Description/index.html'


def test_iGEM_URL():
    config = {
        'src_dir': 'tests/data',
        'build_dir': 'tests/build',
        'team': 'BITSPilani-Goa_India',
        'year': str(date.today().year),
        'silence_warnings': False
    }

    upload_map = {
        'html': {
            'index.html': {
                'link_URL': 'https://2020.igem.org/Team:BITSPilani-Goa_India'
            }
        },
        'assets': {
            'assets/img/logo.jpg': {
                'link_URL': 'https://2020.igem.org/somerandomURLthatiGEMgives'
            }
        }
    }

    assert \
        iGEM_URL(
            config,
            'index.html',
            upload_map,
            'css/style.css') \
        == \
        'https://2020.igem.org/Template:BITSPilani-Goa_India/css/styleCSS?action=raw&ctype=text/css'

    assert \
        iGEM_URL(
            config,
            'index.html',
            upload_map,
            'index.js') \
        == \
        'https://2020.igem.org/Template:BITSPilani-Goa_India/indexJS?action=raw&ctype=text/javascript'

    assert \
        iGEM_URL(
            config,
            '.',
            upload_map,
            'index.html') \
        == \
        'https://2020.igem.org/Team:BITSPilani-Goa_India'

    assert \
        iGEM_URL(
            config,
            'index.html',
            upload_map,
            'Description/') \
        == \
        'https://2020.igem.org/Team:BITSPilani-Goa_India/Description'

    assert \
        iGEM_URL(
            config,
            '.',
            upload_map,
            'assets/img/logo.jpg') \
        == \
        'https://2020.igem.org/somerandomURLthatiGEMgives'

    assert \
        iGEM_URL(
            config,
            '.',
            upload_map,
            'assets/img/logo.xyz') \
        == \
        'assets/img/logo.xyz'

    assert \
        iGEM_URL(
            config,
            '.',
            upload_map,
            'https://2020.igem.org') \
        == \
        'https://2020.igem.org'

    assert \
        iGEM_URL(
            config,
            '.',
            upload_map,
            '/') \
        == \
        'https://2020.igem.org/Team:BITSPilani-Goa_India'
