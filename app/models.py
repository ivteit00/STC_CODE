from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func, expression


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(150))
    target_hours = db.Column(db.Float, default=160)
    worked_hours = db.Column(db.Float, default=0)
    flex_time = db.Column(db.Float, default=0)
    vacation_days = db.Column(db.Integer, default=30)
    vacation_days_taken = db.Column(db.Integer, default=0)
    roles_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    vacation_requests = db.relationship('Vacation', backref='user')
    illness = db.relationship('Illness', backref='user')

    def __repr__(self):
        return '<User %r>' % self.full_name


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class Vacation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    approved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Vacation %r>' % self.id


class Illness (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    approved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Illness %r>' % self.user_id
