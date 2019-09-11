from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

from app.models.character import CharacterModel

parser = reqparse.RequestParser()
parser.add_argument('id', help='required to access character info')
parser.add_argument('name', help='Name field required to find right character', required=True)
parser.add_argument('summary')
parser.add_argument('char_type')
parser.add_argument('game_id')
parser.add_argument('lore')
parser.add_argument('strength')
parser.add_argument('reflex')
parser.add_argument('speed')
parser.add_argument('vitality')
parser.add_argument('awareness')
parser.add_argument('willpower')
parser.add_argument('imagination')
parser.add_argument('attunement')
parser.add_argument('faith')
parser.add_argument('luck')
parser.add_argument('charisma')


class CharacterAll(Resource):
    def get(self):
        return 'all characters'


class Character(Resource):
    def get(self):
        return 'character'

    def post(self):
        data = parser.parse_args()
        return 'new character'

    def patch(self):
        return 'changed character'

    def delete(self):
        return 'deleted character'

