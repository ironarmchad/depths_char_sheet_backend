from app import db


class AbilityModel(db.Model):
    __tablename__ = 'abilities'
    id = db.Column(db.Integer, primary_key=True)
    charId = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    name = db.Column(db.String)
    type = db.Column(db.String)
    summary = db.Column(db.String)
    lore = db.Column(db.String)
    macro = db.Column(db.String)

    def __init__(self, char_id):
        self.charId = char_id

    def __repr__(self):
        return f'ID: {self.id}   CHAR_ID: {self.charId}   NAME: {self.name}'

    def add_ability(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_ability(self):
        db.session.delete(self)
        db.session.commit()

    def jsonify_dict(self):
        return {
            'id': self.id,
            'charId': self.charId,
            'name': self.name,
            'type': self.type,
            'summary': self.summary,
            'lore': self.lore,
            'macro': self.macro
        }

    def patch_from_json(self, data):
        if 'name' in data:
            self.name = data['name']

        if 'type' in data:
            self.type = data['type']

        if 'summary' in data:
            self.summary = data['summary']

        if 'lore' in data:
            self.lore = data['lore']

        if 'macro' in data:
            self.macro = data['macro']

        return self

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by_char_id(cls, char_id):
        return cls.query.filter_by(charId=char_id).all()
