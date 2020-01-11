from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.common.auth_guard import get_character_patch, get_character_view
from app.common.error_handling import Error
from app.models.character import CharacterModel


class CharacterNew(Resource):
    @jwt_required
    def get(self):
        owner = get_jwt_identity()
        new_character = CharacterModel(owner).add_character()

        return {'char_id': new_character.id}


class Character(Resource):
    @jwt_required
    def get(self, char_id):
        try:
            character = get_character_view(char_id)
        except Error as err:
            return {'message': err.message}, 400

        return character.jsonify_dict()

    @jwt_required
    def patch(self, char_id):
        data = request.json

        try:
            character = get_character_patch(char_id)
        except Error as err:
            return {'message': err.message}, 400

        character.patch_from_json(data).add_character()

        return character.jsonify_dict()

    @jwt_required
    def delete(self, char_id):
        try:
            character = get_character_patch(char_id)
        except Error as err:
            return {'message': err.message}, 400

        character.delete_character()

        return {'message': 'Character deleted.'}


class CharacterAll(Resource):
    @jwt_required
    def get(self):
        owner = get_jwt_identity()
        characters = CharacterModel.get_all_by_owner(owner)
        if not characters:
            return {"message": "No characters found."}
        else:
            return {"characters": [character.jsonify_dict() for character in characters]}


class CharacterViewable(Resource):
    @jwt_required
    def get(self):
        owner = get_jwt_identity()
        characters = CharacterModel.get_all_by_viewer(owner)
        if not characters:
            return {"message": "No characters found."}
        else:
            return {"characters": [character.jsonify_dict() for character in characters]}
