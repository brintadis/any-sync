"""
Config for tests
"""
import pytest

from webapp.user.models import User
from webapp import create_app


@pytest.fixture(scope='module')
def new_user():
    user = User("test-user@example.com", "mypassword")
    return user


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        yield testing_client
