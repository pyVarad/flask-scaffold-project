""" User Resource Tests.
"""

import pytest
from tests import create_app
from tests import db


user_info = {
    "username": "test-user",
    "lastName": "R",
    "firstName": "Zorro",
    "emailAddress": "test@test.com"
}

updated_user_info = {
    "username": "test-user",
    "lastName": "Robin",
    "firstName": "Hood",
    "emailAddress": "robinhood@smallorange.com"    
}

@pytest.fixture(scope='module')
def test_client():
    app = create_app('config/test.toml')
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    db.init_app(app)

    with app.test_client() as testing_client:
        with app.app_context() as ctx:
            db.init_app(app)
            db.create_all()
            yield testing_client
            db.drop_all()


def test_add_user(test_client):
    """
    GIVEN The application is up and running.
    WHEN Upon calling the user api to add a new user.
    THEN A new user must be added to the user database.
    """
    create_user = test_client.post('/users', json=user_info)
    assert create_user.status_code == 201
    get_users = test_client.get('/users')
    assert get_users.status_code == 200
    assert len(get_users.get_json().get('users')) == 1
    validate_user_info(test_client, user_info.get('username'))


def test_update_user_info(test_client):
    """
    GIVEN The application is up and running.
    WHEN Upon "put" api to update user information of an existing user.
    AND the requested username exists.
    THEN the user information is updated for the given username.
    """    
    update_user = test_client.put('/user/test-user', json=updated_user_info)
    assert update_user.status_code == 201    
    validate_user_info(test_client, updated_user_info.get('username'), test_update=True)


def test_delete_user(test_client):
    """
    GIVEN The application is up and running.
    WHEN DELETE request is invoked to delete an user by username.
    AND the requested username exists.
    THEN the user is deleted from the database.
    """        
    delete_user = test_client.delete('/user/test-user')
    assert delete_user.status_code == 200   
    get_users = test_client.get('/users')
    assert get_users.status_code == 200
    assert len(get_users.get_json().get('users')) == 0  


def test_delete_non_existing_username_return_400(test_client):
    """
    GIVEN The application is up and running.
    WHEN DELETE request is triggered for a user.
    AND the requested username does not exists.
    THEN return an error message with status code of 400.
    """        
    delete_user = test_client.delete('/user/invalid-user')
    assert delete_user.status_code == 400    


def test_add_existing_username_return_400(test_client):
    """
    GIVEN The application is up and running.
    WHEN POST request is triggered to add a new user
    AND the requested username exists.
    THEN return an error message with status code of 400.
    """        
    new_user = user_info.copy()
    new_user.update({"username": "new-user"})
    create_user = test_client.post('/users', json=new_user)
    assert create_user.status_code == 201
    create_user = test_client.post('/users', json=new_user)
    assert create_user.status_code == 400
    test_client.delete('/user/new-user')


def test_update_non_existing_username_return_400(test_client):
    """
    GIVEN The application is up and running.
    WHEN PUT request is triggered to update a new user with latest userInfo.
    AND the requested username does not exists.
    THEN return an error message with status code of 400.
    """            
    create_user = test_client.put('/user/invalid-user', json=user_info)
    assert create_user.status_code == 400 


def test_get_non_existing_username_return_400(test_client):
    """
    GIVEN The application is up and running.
    WHEN GET request is triggered to delete an user.
    AND the requested username does not exists.
    THEN return an error message with status code of 400.
    """      
    get_user = test_client.get('/user/invalid-user')
    assert get_user.status_code == 400    


def validate_user_info(test_client, username, test_update=False):
    user = test_client.get(f"/user/{username}");
    assert user.status_code == 200

    user_data = user.get_json()

    if test_update:
        assert user_data.get('username') == updated_user_info.get('username') 
        assert user_data.get('firstName') == updated_user_info.get('firstName') 
        assert user_data.get('lastName') == updated_user_info.get('lastName') 
        assert user_data.get('emailAddress') == updated_user_info.get('emailAddress')         
    else:
        assert user_data.get('username') == user_info.get('username') 
        assert user_data.get('firstName') == user_info.get('firstName') 
        assert user_data.get('lastName') == user_info.get('lastName') 
        assert user_data.get('emailAddress') == user_info.get('emailAddress') 