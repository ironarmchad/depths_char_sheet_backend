from flask import request
from flask_restful import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

from app.models.character import CharacterModel


class Error(Exception):
    def __init__(self):
        self.message = 'Error has occurred.'


class NotFoundError(Error):
    def __init__(self):
        self.message = 'Character could not be found.'


class NotOwnerError(Error):
    def __init__(self):
        self.message = 'Cannot access another players character.'


def get_character(char_id):
    character = CharacterModel.get_by_id(char_id)

    if not character:
        raise NotFoundError()
    elif character.owner != get_jwt_identity():
        raise NotOwnerError()
    else:
        return character


class CharacterNew(Resource):
    @jwt_required
    def post(self):
        owner = get_jwt_identity()
        new_character = CharacterModel(owner)

        new_character.patch_from_json(request.json)

        new_character.add_character()

        return new_character.jsonify_dict()


class Character(Resource):
    @jwt_required
    def get(self, char_id):
        try:
            character = get_character(char_id)
        except Error as err:
            return {'message': err.message}, 400

        return character.jsonify_dict()

    @jwt_required
    def patch(self, char_id):
        data = request.json

        try:
            character = get_character(char_id)
        except Error as err:
            return {'message': err.message}, 400

        character.patch_from_json(data).add_character()

        return character.jsonify_dict()

    @jwt_required
    def delete(self, char_id):
        try:
            character = get_character(char_id)
        except Error as err:
            return {'message': err.message}, 400

        character.delete_character()

        return {'message': 'Character deleted.'}
