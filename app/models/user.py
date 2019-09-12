from marshmallow import Schema, fields, post_load
from passlib.hash import pbkdf2_sha256 as sha256

from app import db, marsh


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'ID: {self.id} USERNAME: {self.username}'

    def __eq__(self, other):
        return self.username == other.username

    def __lt__(self, other):
        return self.username < other.username

    def add_user(self):
        self.password = sha256.hash(self.password)
        db.session.add(self)
        db.session.commit()
        return self

    def check_password(self, password):
        return sha256.verify(password, self.password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


class UserSchema(marsh.ModelSchema):
    class Meta:
        model = UserModel
