from app import db


class GameModel(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True)
    st_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    active = db.Column(db.Boolean, nullable=False)
    lore = db.Column(db.String)
    summary = db.Column(db.String(150))

    def __init__(self, st_id):
        self.st_id = st_id
        self.active = False
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'ID: {self.id} NAME: {self.name} ST_ID: {self.st_id}'

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'st_id': self.st_id,
            'active': self.active,
            'lore': self.lore,
            'summary': self.summary
        }

    def patch_from_json(self, data):
        if 'name' in data:
            self.name = data['name']

        if 'active' in data:
            self.active = data['active']

        if 'lore' in data:
            self.lore = data['lore']

        if 'summary' in data:
            self.summary = data['summary']

        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        games = GameModel.query.order_by(GameModel.name).all()
        return {'games': list(map(lambda x: x.to_json(), games))}
