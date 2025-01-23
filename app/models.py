from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
db = SQLAlchemy()

class Park(db.Model):
    __tablename__ = 'parks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

    trails = db.relationship('Trail', backref='parks', lazy=True)
    wildlife = db.relationship('Wildlife', backref='parks', lazy=True)
    announcement = db.relationship('Announcement', backref='parks', lazy=True)
    #feedbacks = db.relationship('Feedback', backref='parks', lazy=True)

    def to_dict(self):
        """Converts a Park object to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'image_url': self.image_url
        }


class Trail(db.Model):
    __tablename__ = 'trails'

    trail_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.id'), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    def __repr__(self):
        return f"<Trail {self.name}>"


class Wildlife(db.Model):
    __tablename__ = 'wildlife'

    wildlife_id = db.Column(db.Integer, primary_key=True)
    species_name = db.Column(db.String(100), nullable=False)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    def __repr__(self):
        return f"<Wildlife {self.species_name}>"


class Announcement(db.Model):
    __tablename__ = 'announcements'

    announcement_id = db.Column(db.Integer, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    def __repr__(self):
        return f"<Announcement {self.title}>"


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")
    points = db.Column(db.Integer, default=0)
    badges = db.relationship('UserBadges', back_populates='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Badge(db.Model):
    __tablename__ = 'badges'

    badge_id = db.Column(db.Integer, primary_key=True)
    badge_name = db.Column(db.String(50), unique=True, nullable=False)
    points_required = db.Column(db.Integer, nullable=False)

    awarded_users = db.relationship('UserBadges', back_populates='badge', lazy=True)

    def __repr__(self):
        return f"<Badge {self.badge_name}>"


class UserBadges(db.Model):
    __tablename__ = 'user_badges'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.badge_id'), primary_key=True)
    badge_name = db.Column(db.String(100), unique=True, nullable=False)

    user = db.relationship('User', back_populates='badges')
    badge = db.relationship('Badge', back_populates='awarded_users')


class Feedback(db.Model):
    __tablename__ = 'feedback'

    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.id'), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    user = db.relationship('User', backref='feedbacks', lazy=True)
    park = db.relationship('Park', backref='feedback_list', lazy=True)

    def __repr__(self):
        return f"<Feedback {self.feedback_id}>"


class Booking(db.Model):
    __tablename__ = 'bookings'

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity = db.Column(db.String(255), nullable=False)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False)

    user = db.relationship('User', backref='bookings', lazy=True)
    park = db.relationship('Park', backref='bookings', lazy=True)

    def __repr__(self):
        return f"<Booking {self.booking_id}: {self.activity} at Park {self.park_id}>"