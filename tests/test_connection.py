import requests


def test_connection():
    """Runs a basic test to check connection. """

    response = requests.get('https://igem.org')
    assert response.status_code == 200
