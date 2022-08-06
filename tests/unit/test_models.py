"""
Testing models
"""


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """
    assert new_user.email == "test-user@example.com"
    assert new_user.set_password != "mypassword"
