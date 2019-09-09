from app import db


class GameModel(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, index=True)
    st_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    active = db.Column(db.Boolean, nullable=False)
    lore = db.Column(db.String)
    summary = db.Column(db.String(150))

    def __init__(self, st_id):
        self.st_id = st_id
        db.session.add(self)
        db.session.commit(self)

    def __repr__(self):
        return repr(self.to_json())

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

    @classmethod
    def return_all(cls):
        games = GameModel.query.all().order_by(GameModel.name)
        return {'games': list(map(lambda x: x.to_json(), games))}
