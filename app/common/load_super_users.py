from app.models.user import UserModel


def load_super_users():
    if UserModel.get_by_username('ironarmchad') is None:
        user = UserModel('ironarmchad', 'temppassword')
        user.type = 'super'
        user.add_user()

    if UserModel.get_by_username('cyrilkhan') is None:
        user = UserModel('cyrilkhan', 'temppassword')
        user.type = 'super'
        user.add_user()
