from tests.conftest import random_string
from app.models.user import UserModel



# __init__ should create a user with username and password
def test_init():
    username = random_string()
    password = random_string()
    user = UserModel(username, password)
    assert user.username == username and user.password == password

# __repr__ should print a string with username
def test_repr():
    username = random_string()
    user = UserModel(username, 'test')

    assert username in repr(user)

# jsonify_dict should return a dict that has 'id' key and 'username' key
def test_jsonify_dict_keys():
    user = UserModel('test', 'test')

    json = user.jsonify_dict()

    assert 'id' in json and 'username' in json

# jsonify_dict should have username stored as 'username' in dict
def test_jsonify_dict_username():
    username = random_string()
    user = UserModel(username, 'test')

    json = user.jsonify_dict()

    assert json['username'] == username

# jsonify_dict should have id created by the database
def test_jsonify_dict_id(app):
    user = UserModel('test1', 'test')

    assert user.jsonify_dict()['id'] == None

    with app.app_context():
        user.add_user()

        assert user.jsonify_dict()['id'] != None


# add_user should store user in database
def test_add_user_db(app):
    username = random_string()
    password = random_string()
    with app.app_context():
        user = UserModel(username, password)

        user.add_user()

        assert UserModel.query.filter_by(username=username).first().username == username

# add_user should not store the raw password
def test_add_user_password(app):
    username = random_string()
    password = random_string()
    with app.app_context():
       user = UserModel(username, password)

       user.add_user()

       assert UserModel.query.filter_by(username=username).first().password != password

# check_password should return true if password string matches original password
def test_check_password(app):
    username = random_string()
    password = random_string()
    with app.app_context():
        user = UserModel(username, password)
        user.add_user()

        assert user.check_password(password)

# find_by_username should return the user with the asked for username
def test_find_by_username(app):
    username = random_string()
    with app.app_context():
        user = UserModel(username, 'test')
        user.add_user()

        assert UserModel.find_by_username(username).username == username

