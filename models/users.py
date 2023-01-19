from api_lib.db import db


class UsersModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    is_privileged = db.Column(db.Boolean, default=False)
