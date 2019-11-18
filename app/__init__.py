from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS


db = SQLAlchemy()
login = LoginManager()


def create_app(config_type):
    app = Flask(__name__, template_folder='templates', static_folder='static', instance_relative_config=True)

    config = {
        'dev': 'app.config.DevelopmentConfig'
    }

    # Config setup
    app.config.from_object(config[config_type])
    app.config.from_pyfile('config.cfg', silent=True)

    # Service start-up
    api = Api(app)
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    login.init_app(app)
    CORS(app, supports_credentials=True)

    # Views
    from app.views.main import admin_main
    app.register_blueprint(admin_main)

    # Resources
    from app.resources.user import UserAvailable
    api.add_resource(UserAvailable, '/user/available')

    from app.resources.user import User
    api.add_resource(User, '/user')

    from app.resources.user import UserRegister
    api.add_resource(UserRegister, '/user/register')

    from app.resources.user import UserLogin
    api.add_resource(UserLogin, '/user/login')

    from app.resources.character import CharacterAll
    api.add_resource(CharacterAll, '/character/all')

    from app.resources.character import CharacterNew
    api.add_resource(CharacterNew, '/character/new')

    from app.resources.character import Character
    api.add_resource(Character, '/character/get/<char_id>')

    return app
