from app import db


class CharacterModel(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), index=True)
    lore = db.Column(db.JSON)
    stats = db.Column(db.JSON)
    abilities = db.Column(db.JSON)

    def __init__(self, owner_id):
        self.owner_id = owner_id

    # Representations
    def __repr__(self):
        return f'ID: {self.id} OWNER: {self.owner} NAME: {self.name}'

    def jsonify_dict(self):
        return {
            'id': self.id,
            'ownerId': self.owner_id,
            'name': self.name,
            'lore': self.lore,
            'stats': self.stats,
            'abilities': self.abilities
        }

    # Mutate entity methods
    def patch_from_json(self, data):
        if 'name' in data:
            self.name = data['name']

        if 'lore' in data:
            self.lore = data['lore']

        if 'stats' in data:
            self.stats = data['stats']

        if 'abilities' in data:
            self.abilities = data['ablilities']

        return self

    # Mutate database methods
    def add_character(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_character(self):
        db.session.delete(self)
        db.session.commit()
        return self

    # Database access methods
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all_by_owner(cls, owner_id):
        return cls.query.filter_by(owner_id=owner_id).all()
