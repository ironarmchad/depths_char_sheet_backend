from passlib.hash import pbkdf2_sha256 as sha256

from app import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = sha256.hash(password)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'ID: {self.id} USERNAME: {self.username}'

    def __eq__(self, other):
        return self.username == other.username

    def __lt__(self, other):
        return self.username < other.username

    def to_json(self):
        return {
            'username': self.username,
        }

    def check_password(self, password):
        return sha256.verify(password, self.password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def return_all(cls):
        users = cls.query.order_by(UserModel.username).all()
        return {'users': list(map(lambda x: x.to_json(), users))}
