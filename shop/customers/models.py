from datetime import datetime

from shop import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    dob = db.Column(db.DateTime, unique=False)
    civ_id = db.Column(db.String(50), unique=True)
    phone_number = db.Column(db.String(50), unique=True)
    profile_pic = db.Column(db.String(200), unique=False, default="profile.jpg")
    reg_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<Customer %r>" % self.title

db.create_all()