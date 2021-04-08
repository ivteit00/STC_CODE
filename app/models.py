from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    full_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.relationship('role', db.ForeignKey('roles.id'))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    role_name = db.Column(db.String(64), nullable=False)
