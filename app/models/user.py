from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256 as sha256

from app import db


class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = sha256.hash(password)
        self.type = 'normal'

    # Representations
    def __repr__(self):
        return f'ID: {self.id} USERNAME: {self.username}'

    def jsonify_dict(self):
        return {'id': self.id, 'username': self.username}

    def check_password(self, password):
        return sha256.verify(password, self.password)

    # Mutate instance
    def change_username(self, username):
        self.username = username
        return self

    def change_password(self, password):
        self.password = sha256.hash(password)
        return self

    # Mutate database
    def add_user(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
        return self

    # Database accessors
    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.username).all()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
