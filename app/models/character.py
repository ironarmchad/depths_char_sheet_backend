from app import db, marsh


class CharacterModel(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), index=True)
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
        db.session.commit()

    def __repr__(self):
        return f'ID: {self.id} OWNER: {self.owner} NAME: {self.name}'

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
            'strength': self.strength,
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

    def patch_from_json(self, data):
        if 'name' in data:
            self.name = data['name']

        if 'summary' in data:
            self.summary = data['summary']

        if 'char_type' in data:
            self.char_type = data['char_type']

        if 'game_id' in data:
            self.game_id = data['game_id']

        if 'lore' in data:
            self.lore = data['lore']

        if 'strength' in data:
            self.strength = data['strength']

        if 'reflex' in data:
            self.reflex = data['reflex']

        if 'speed' in data:
            self.speed = data['speed']

        if 'vitality' in data:
            self.vitality = data['vitality']

        if 'awareness' in data:
            self.awareness = data['awareness']

        if 'willpower' in data:
            self.willpower = data['willpower']

        if 'imagination' in data:
            self.imagination = data['imagination']

        if 'attunement' in data:
            self.attunement = data['attunement']

        if 'faith' in data:
            self.faith = data['faith']

        if 'luck' in data:
            self.luck = data['luck']

        if 'charisma' in data:
            self.charisma = data['charisma']

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)


class CharacterSchema(marsh.ModelSchema):
    class Meta:
        model = CharacterModel
