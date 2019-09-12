from app.models.user import UserModel, UserSchema


def test_repr(app):
    with app.app_context():
        user = UserModel.query.get(1)

    assert repr(user) == 'ID: 1 USERNAME: test'


def test_comp(app):
    with app.app_context():
        user1 = UserModel.query.get(1)
        user2 = UserModel('test2', 'test2').add_user()
        assert not user1 == user2
        assert user1 < user2

def test_check_password(app):
    with app.app_context():
        user = UserModel.query.get(1)
        assert user.check_password('test')


def test_find_by_username(app):
    with app.app_context():
        user = UserModel.find_by_username('test')
        assert user.id == 1

def test_user_schema(app):
    with app.app_context():
        user = UserModel.query.get(1)
        json = UserSchema().dump(user)
        for key in json:
            assert user.__getattribute__(key) == json[key]

        data = {
            'username': 'test2',
            'password': 'test2'
        }
        user2 = UserSchema().load(data)
        assert user2.username == data['username']
        assert user2.password == data['password']