from flask_restful import Resource

from app.models.compendium import CompendiumModel


class Compendium(Resource):
    def get(self, compendium_id):
        return CompendiumModel.get_by_id(compendium_id).jsonify_dict()


class CompendiumAll(Resource):
    def get(self):
        pages = CompendiumModel.get_all()
        return {"pages": [page.jsonify_short() for page in pages]}
