from app import create_app
from app.common.load_super_users import load_super_users

if __name__ == '__main__':
    app = create_app('dev')

    with app.app_context():
        load_super_users()

    app.run()
