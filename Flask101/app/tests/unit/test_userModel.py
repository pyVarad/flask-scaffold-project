from tests import User


def test_new_user():
    """
    GIVEN a User model.
    WHEN a new user is created.
    THEN "username", "firstName", "lastName" and "emailAddress" are a part of the instance of User object.
    """
    user = User(username = 'aloha', 
        lastName = 'jerry', 
        firstName = 'Alex', 
        emailAddress = 'jerry@alex.com'
        )
    assert user.username == 'aloha'
    assert user.lastName == 'jerry'
    assert user.firstName == 'Alex'
    assert user.emailAddress == 'jerry@alex.com'