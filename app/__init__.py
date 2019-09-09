from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile(f'../config/dev.py')

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

CORS(app, resources={r"/*": {"origins": "*"}})

from app.resources.user_validator import UsernameAvailable
api.add_resource(UsernameAvailable, '/user/available')

from app.resources.user import AllUsers
api.add_resource(AllUsers, '/user')

from app.resources.user import UserRegistration
api.add_resource(UserRegistration, '/user/register')

from app.resources.user import UserLogin
api.add_resource(UserLogin, '/user/login')

from app.resources.user import SecretResource
api.add_resource(SecretResource, '/secret')

from app.resources.character import CharacterAll
api.add_resource(CharacterAll, '/character/all')

from app.resources.character import Character
api.add_resource(Character, '/character')

from app.resources.game import Game
api.add_resource(Game, '/game')
