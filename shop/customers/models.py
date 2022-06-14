from datetime import datetime
from flask_login import UserMixin
import json

from shop import db, login_manager


@login_manager.user_loader
def user_loader(user_id):
    return Customer.query.get(user_id)

class Customer(db.Model, UserMixin):
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
        return "<Customer %r>" % self.username

class JsonDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return "{}"
        
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}

        return json.loads(value)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default="Pending", nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    invoice_details = db.Column(JsonDict)

    def __repr__(self):
        return "<Invoice %r>" % self.invoice_number

db.create_all()
