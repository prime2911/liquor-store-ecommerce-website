from wtforms import Form, TextAreaField, StringField, PasswordField, SubmitField, validators
from wtforms.fields.datetime import DateField
from flask_wtf.file import FileAllowed, FileField, FileRequired


class CustomerRegistrationForm(Form):
    name = StringField("Name", [validators.Length(min=4, max=200)])
    username = StringField("Username", [validators.Length(min=4, max=200), validators.DataRequired()])
    email = StringField(
        "Email Address", [validators.Length(min=6, max=200), validators.Email(), validators.DataRequired()])
    password = PasswordField("Password", [
        validators.DataRequired(),
        validators.EqualTo("confirm", message="Passwords must match!")
    ])
    confirm = PasswordField("Confirm Password", [validators.DataRequired()])
    dob = DateField("Date of Birth", [validators.DataRequired()], "%Y-%m-%d")
    civ_id = StringField("Citizen Identification Number", [validators.Length(min=4, max=50), validators.DataRequired()])
    phone_number = StringField("Phone Number", [validators.Length(min=4, max=50), validators.DataRequired()])

    profile_pic = FileField("Profile Picture", [FileAllowed(["jpg", "png", "jpeg"], "Only images allowed!")])
    submit = SubmitField("Register")
