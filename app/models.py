from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, creator, user

    # Use back_populates to avoid backref conflict
    registrations = db.relationship('EventRegistration', back_populates='user', lazy=True)
    events = db.relationship('Event', back_populates='creator', lazy=True)  # relationship to Event


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # Event name
    description = db.Column(db.Text, nullable=False)   # Other details
    date = db.Column(db.DateTime, nullable=False)      # Date of the event
    venue = db.Column(db.String(150), nullable=False)  # Venue of the event
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User who created

    # back_populates instead of backref
    creator = db.relationship('User', back_populates='events')

    registrants = db.relationship('EventRegistration', back_populates='event', lazy='dynamic')

    def registration_count(self):
        return self.registrants.count()


class EventRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # back_populates matching those above, removing backref conflicts
    event = db.relationship('Event', back_populates='registrants')
    user = db.relationship('User', back_populates='registrations')

    def __repr__(self):
        return f"<Registration User {self.user_id} -> Event {self.event_id}>"
