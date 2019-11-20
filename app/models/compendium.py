from app import db


class CompendiumModel(db.Model):
    __tablename__ = 'compendium'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String, index=True)
    content = db.Column(db.String)

    def __init__(self, owner_id, title):
        self.owner_id = owner_id
        self.title = title
        self.content = ""

    # Representation
    def jsonify_dict(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'title': self.title,
            'content': self.content
        }

    def jsonify_short(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'title': self.title
        }

    # Mutate entity methods
    def patch_from_json(self, data):
        if 'title' in data:
            self.title = data['title']

        if 'content' in data:
            self.content = data['content']

        return self

    # Mutate database methods
    def add_compendium(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_compendium(self):
        db.session.delete(self)
        db.session.commit()
        return self

    # Database access methods
    @classmethod
    def get_by_id(cls, compendium_id):
        return cls.query.get(compendium_id)

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.title).all()

    @classmethod
    def get_all_by_owner(cls, owner_id):
        return cls.query.order_by(cls.title).all()
