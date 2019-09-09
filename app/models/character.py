from app import db


class CharacterModel(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    summary = db.Column(db.String(150))
    char_type = db.Column(db.String(10))
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    lore = db.Column(db.String)
    strength = db.Column(db.Integer)
    reflex = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    vitality = db.Column(db.Integer)
    awareness = db.Column(db.Integer)
    willpower = db.Column(db.Integer)
    imagination = db.Column(db.Integer)
    attunement = db.Column(db.Integer)
    faith = db.Column(db.Integer)
    luck = db.Column(db.Integer)
    charisma = db.Column(db.Integer)

    def __init__(self, owner):
        self.owner = owner
        db.session.add(self)
        db.session.commit(self)

    def __repr__(self):
        return repr(self.to_json())

    def __str__(self):
        return str(self.to_json())

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def to_json(self):
        return {
            'id': self.id,
            'owner': self.owner,
            'name': self.name,
            'summary': self.summary,
            'char_type': self.char_type,
            'game_id': self.game_id,
            'lore': self.lore,
            'strength': self.game_id,
            'reflex': self.reflex,
            'speed': self.speed,
            'vitality': self.vitality,
            'awareness': self.awareness,
            'willpower': self.willpower,
            'imagination': self.imagination,
            'attunement': self.attunement,
            'faith': self.faith,
            'luck': self.luck,
            'charisma': self.charisma
        }