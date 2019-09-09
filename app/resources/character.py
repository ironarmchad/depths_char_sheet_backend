from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

from app.models.character import CharacterModel

parserNew = reqparse.RequestParser()

parserMod = reqparse.RequestParser()
parserMod.add_argument('name', help='Name field required to find right character', required=True)


class CharacterAll(Resource):
    def get(self):
        return 'all characters'


class Character(Resource):
    def get(self):
        return 'character'

    def post(self):
        return 'new character'

    def patch(self):
        return 'changed character'

    def delete(self):
        return 'deleted character'

