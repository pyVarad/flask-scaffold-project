from tests import create_app
from tests import db


app = create_app('config/test.toml')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
db.init_app(app)


def test_add_user():
    with app.app_context():
        db.create_all()

        with app.test_client() as test_client:
            create_user = test_client.post(
                '/users', json={
                    "username": "test-user",
                    "lastName": "R",
                    "firstName": "Zorro",
                    "emailAddress": "test@test.com"
                    }
                )
            assert create_user.status_code == 201
    
            get_users = test_client.get('/users')
            assert get_users.status_code == 200
            assert len(get_users.get_json().get("users")) == 1
    
            get_user = test_client.get('/user/test-user')
            assert get_user.status_code == 200
    
            userInfo = get_user.get_json()
            assert userInfo.get("username") == "test-user"
            assert userInfo.get("lastName") == "R"
            assert userInfo.get("firstName") == "Zorro"
            assert userInfo.get("emailAddress") == "test@test.com"            

        db.drop_all()


def test_update_user():
    with app.app_context():
        db.create_all()

        with app.test_client() as test_client:
            create_user = test_client.post(
                '/users', json={
                    "username": "test-user",
                    "lastName": "R",
                    "firstName": "Zorro",
                    "emailAddress": "test@test.com"
                    }
                )
            assert create_user.status_code == 201

            get_users = test_client.get('/users')
            assert get_users.status_code == 200
            assert len(get_users.get_json().get("users")) == 1

            get_user = test_client.get('/user/test-user')
            assert get_user.status_code == 200

            userInfo = get_user.get_json()
            assert userInfo.get("username") == "test-user"
            assert userInfo.get("lastName") == "R"
            assert userInfo.get("firstName") == "Zorro"
            assert userInfo.get("emailAddress") == "test@test.com"

            userInfo.update({"emailAddress": "johnny@zorro.com"})
            put_user = test_client.put('/user/test-user', json=userInfo)
            assert put_user.status_code == 201

            get_user = test_client.get('/user/test-user')
            assert get_user.status_code == 200      

            userInfo = get_user.get_json()
            assert userInfo.get("username") == "test-user"
            assert userInfo.get("lastName") == "R"
            assert userInfo.get("firstName") == "Zorro"
            assert userInfo.get("emailAddress") == "johnny@zorro.com"

            put_user_for_invalid_user = test_client.put('/user/user-not-found', json=userInfo)
            assert put_user_for_invalid_user.status_code == 400                      

        db.drop_all()


def test_delete_user():
    with app.app_context():
        db.create_all()

        with app.test_client() as test_client:
            create_user = test_client.post(
                '/users', json={
                    "username": "test-delete-user",
                    "lastName": "R",
                    "firstName": "Zorro",
                    "emailAddress": "test@test.com"
                    }
                )
            assert create_user.status_code == 201

            get_users = test_client.get('/users')
            assert get_users.status_code == 200
            assert len(get_users.get_json().get("users")) == 1

            del_user = test_client.delete('/user/test-delete-user')
            assert del_user.status_code == 200

            get_users = test_client.get('/users')
            assert get_users.status_code == 200
            assert len(get_users.get_json().get("users")) == 0   

            del_user = test_client.delete('/user/user-not-found')
            assert del_user.status_code == 400

        db.drop_all()    