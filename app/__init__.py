from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
marsh = Marshmallow()


def create_app(config_over=None):
    app = Flask(__name__)
    app.config.from_pyfile(f'../config/dev.py')

    if config_over:
        app.config.from_mapping(config_over)

    api = Api(app)
    db.init_app(app)
    marsh.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    CORS(app, supports_credentials=True)

    app.config['CORS_HEADERS'] = 'Content-Type'

    from app.resources.hello import Hello
    api.add_resource(Hello, '/hello')

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

    from app.resources.game import Game
    api.add_resource(Game, '/game')

    return app


'''
    from app.resources.character import CharacterAll
    api.add_resource(CharacterAll, '/character/all')
'''
