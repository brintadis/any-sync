"""
Testing views
"""


def test_home_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'AnySync' in response.data
    assert b'Spotify' in response.data
    assert b'Yandex Music' in response.data


def test_home_page_post(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post('/')
    assert response.status_code == 405
    assert b'AnySync' not in response.data
