from flask_restful import Resource, reqparse

from app.models.user import UserModel

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)


class UsernameAvailable(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'available': False}
        return {'available': True}
