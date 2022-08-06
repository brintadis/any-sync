"""
Config for tests
"""
import pytest

from webapp.user.models import User
from webapp import create_app


@pytest.fixture(scope='module')
def new_user():
    """
    Create new user
    """
    email = "test-user@example.com"
    password = "mypassword"
    user = User(
        email=email
    )
    user.set_password(password)
    return user


@pytest.fixture(scope='module')
def test_client():
    """
    Testing flask app client
    """
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        yield testing_client
