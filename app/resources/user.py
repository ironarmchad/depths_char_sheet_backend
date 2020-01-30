from flask import request
from flask_restful import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)

from app.models.user import UserModel


class User(Resource):
    @jwt_required
    def get(self):
        user = UserModel.get_by_id(get_jwt_identity())
        return user.jsonify_dict()


class UserInfo(Resource):
    @jwt_required
    def get(self):
        user = UserModel.get_by_id(get_jwt_identity())
        return {user.info}, 200

    @jwt_required
    def post(self, info):
        user = UserModel.get_by_id(get_jwt_identity())
        print(info)
        return {'msg': 'User updated.'}, 200


class UserAll(Resource):
    @jwt_required
    def get(self):
        users = UserModel.get_all()

        return [{'id': user.id, 'username': user.username} for user in users]


class UserAvailable(Resource):
    def post(self):
        data = request.json

        if not 'username' in data:
            return {'message': 'Must include username'}, 400
        elif UserModel.username_available(data['username']):
            return {'available': True}
        else:
            return {'available': False}


class UserRegister(Resource):
    def post(self):
        data = request.get_json()

        if not 'username' in data or not 'password' in data:
            return {'message': 'username and password must be provided.'}, 400

        if UserModel.get_by_username(data['username']):
            return {'message': 'username must be unique'}, 400

        user = UserModel(data['username'], data['password']).add_user()
        return {
            'username': data['username'],
            'accessToken': create_access_token(identity=user.id),
            'refreshToken': create_refresh_token(identity=user.id)
        }


class UserLogin(Resource):
    def post(self):
        data = request.json

        if not 'username' in data or not 'password' in data:
            return {'message': 'username and password must be provided.'}, 400

        current_user = UserModel.get_by_username(data['username'])

        if not current_user:
            return {
                       'message': f'User {data["username"]} doesn\'t exist.'
                   }, 400
        elif not current_user.check_password(data['password']):
            return {
                       'message': f'Password doesn\'t match.'
                   }, 400
        else:
            return {
                'username': current_user.username,
                'info': current_user.info,
                'accessToken': create_access_token(identity=current_user.id),
                'refreshToken': create_access_token(identity=current_user.id)
            }
