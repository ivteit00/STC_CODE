from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(150))
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r,' % self.full_name + 'role %r' % self.roles_id


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r, ' % self.name + 'id %r' % self.id + '>'


class VacationRequest(db.Model):
    __tablename__ = 'vacation'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    approved = db.Column(db.Boolean)
