from wtforms import Form, StringField, PasswordField, validators


class RegistrationForm(Form):
    name = StringField("Name", [validators.Length(min=4, max=200)])
    username = StringField("Username", [validators.Length(min=4, max=200), validators.DataRequired()])
    email = StringField(
        "Email Address", [validators.Length(min=6, max=200), validators.Email()])
    password = PasswordField("Password", [
        validators.DataRequired(),
        validators.EqualTo("confirm", message="Passwords must match!")
    ])
    confirm = PasswordField("Confirm Password")


class LoginForm(Form):
    email = StringField(
        "Email Address", [validators.Length(min=6, max=200), validators.Email()])
    password = PasswordField("Password", [validators.DataRequired()])
