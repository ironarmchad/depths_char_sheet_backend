from app.models.user import UserModel


def test_repr(app):
    with app.app_context():
        user = UserModel.query.get(1)

    assert repr(user) == 'ID: 1 USERNAME: test'


def test_comp(app):
    with app.app_context():
        user1 = UserModel.query.get(1)
        user2 = UserModel('test2', 'test2')
        assert not user1 == user2
        assert user1 < user2


def test_to_json(app):
    with app.app_context():
        user = UserModel.query.get(1)
        assert user.to_json()['username'] == 'test'


def test_check_password(app):
    with app.app_context():
        user = UserModel.query.get(1)
        assert user.check_password('test')


def test_find_by_username(app):
    with app.app_context():
        user = UserModel.find_by_username('test')
        assert user.id == 1


def test_return_all(app):
    with app.app_context():
        UserModel('test2', 'test2')
        assert len(UserModel.return_all()['users']) == 2
