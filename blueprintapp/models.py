from flask_login import UserMixin

from app import db

class User(db.Model, UserMixin):
    __tablename__ == 'users'

    uid = db.Column(Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f'<User: {self.username}'

    def get_id(self):
        return self.uid