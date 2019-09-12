from flask import request
from flask_restful import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

from app.models.user import UserModel, UserSchema


class User(Resource):
    @jwt_required
    def get(self):
        user = UserModel.query.get(get_jwt_identity())
        return UserSchema(exclude=['password']).dump(user)

    '''    
    @jwt_required
    def post(self):
        user = UserModel.query.get(get_jwt_identity())
        data = UserSchema().loads(request.data)
        
        if UserModel.find_by_username(data.username):
            return {'message': 'username must be unique'}, 400
        else:
            data.id = user.id
            data.add_user()
            return {'message': f'User {data.username} updated'}
    '''


class UserAvailable(Resource):
    def post(self):
        data = request.json

        if not 'username' in data:
            return {'message': 'Must include username'}, 400
        elif UserModel.find_by_username(data['username']):
            return {'available': False}
        else:
            return {'available': True}


class UserRegister(Resource):
    def post(self):
        data = UserSchema().load(request.json)

        if UserModel.find_by_username(data.username):
            return {'message': 'username must be unique'}, 400

        data.add_user()
        return {
            'username': data.username,
            'accessToken': create_access_token(identity=data.id),
            'refreshToken': create_refresh_token(identity=data.id)
        }


class UserLogin(Resource):
    def post(self):
        data = UserSchema().loads(request.data)
        current_user = UserModel.find_by_username(data.username)

        if not current_user:
            return {
                       'message': f'User {data.username} doesn\'t exist.'
                   }, 400
        elif not current_user.check_password(data.password):
            return {
                       'message': f'Password doesn\'t match.'
                   }, 400
        else:
            return {
                'username': current_user.username,
                'accessToken': create_access_token(identity=current_user.id),
                'refreshToken': create_access_token(identity=current_user.id)
            }


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
