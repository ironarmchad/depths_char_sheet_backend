from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_pyfile(f'../config/{config_name}.py')

    api = Api(app)
    db.init_app(app)
    jwt.init_app(app)

    @app.before_first_request
    def create_db():
        db.create_all()

    from app.resources.user import AllUsers
    api.add_resource(AllUsers, '/user')

    from app.resources.user import UserRegistration
    api.add_resource(UserRegistration, '/user/register')

    from app.resources.user import UserLogin
    api.add_resource(UserLogin, '/user/login')

    from app.resources.user import SecretResource
    api.add_resource(SecretResource, '/secret')

    return app
