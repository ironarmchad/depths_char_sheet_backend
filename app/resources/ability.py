from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.resources import Error, NotFoundError, NotOwnerError, get_character

from app.models.ability import AbilityModel
from app.models.character import CharacterModel


def get_ability(id):
    ability = AbilityModel.get_by_id(id)

    if not ability:
        raise NotFoundError()

    character = CharacterModel.get_by_id(ability.id)

    if character.owner != get_jwt_identity():
        raise NotOwnerError()

    return ability


class Ability(Resource):
    @jwt_required
    def get(self, id):
        try:
            ability = get_ability(id)
        except Error as err:
            return {'message': err.message}, 400

        return ability.jsonify_dict()

    @jwt_required
    def patch(self, id):
        data = request.json

        try:
            ability = get_ability(id)
        except Error as err:
            return {'message': err.message}, 400

        ability.patch_from_json(data['ability']).add_ability()

        return ability.jsonify_dict()

    @jwt_required
    def delete(self, id):
        try:
            ability = get_ability(id)
        except Error as err:
            return {'message': err.message}, 400

        ability.delete_ability()

        return {'message': 'Ability deleted.'}


class AbilityNew(Resource):
    @jwt_required
    def post(self, char_id):
        try:
            get_character(char_id)
        except Error as err:
            return {'message': err.message}, 400

        ability = AbilityModel(char_id)
        ability.patch_from_json(request.json)
        ability.add_ability()

        return ability.jsonify_dict()


class AbilityAll(Resource):
    @jwt_required
    def get(self, char_id):
        try:
            char = get_character(char_id)
        except Error as err:
            return {'message': err.message}, 400

        abilities = AbilityModel.get_by_char_id(char.id)

        return {"abilities": [ability.jsonify_dict() for ability in abilities]}
