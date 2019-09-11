from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

from app.models.user import UserModel

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'UsernameInUse'}, 400

        UserModel(data['username'], data['password'])
        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])
        return {
            'username': data['username'],
            'access-token': access_token,
            'refresh-token': refresh_token
        }


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': f'User {data["username"]} doesn\'t exist'}, 400

        if current_user.check_password(data['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'username': data['username'],
                'accessToken': access_token,
                'refreshToken': refresh_token
            }
        else:
            return {'message': 'Wrong credentials.'}, 400


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
