from app import create_app
from app.models.user import UserModel

if __name__ == '__main__':
    app = create_app('staging')

    with app.app_context():
        if UserModel.get_by_username('ironarmchad') is None:
            user = UserModel('ironarmchad', 'temppassword')
            user.type = 'super'
            user.add_user()

    app.run()
