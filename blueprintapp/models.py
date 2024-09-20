from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from blueprintapp.app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Increased length to handle hashed passwords
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    workouts = db.relationship('Workout', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User: {self.username}>'

    def get_id(self):
        return self.uid

    def set_password(self, password):
        """Set the password for the user after hashing it."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hashed password."""
        return check_password_hash(self.password, password)

class Workout(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    exercises = db.relationship('Exercise', backref='workout', lazy='dynamic')

class Exerciselist(db.Model):
    __tablename__ = 'exerciselist'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    exercise = db.relationship('Exercise', backref='exercise', lazy='dynamic')

class Exercise(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.uid'))
    order = db.Column(db.Integer)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exerciselist.uid'))
    sets = db.relationship('Set', backref='exercise', lazy='dynamic')

class Set(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    weight = db.Column(db.Numeric(precision=2, asdecimal=False, decimal_return_scale=None))
    reps = db.Column(db.Integer)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.uid'))
