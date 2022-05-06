from wtforms import Form, StringField, PasswordField, validators


class RegistrationForm(Form):
    name = StringField("Name", [validators.Length(min=4, max=25)])
    username = StringField("Username", [validators.Length(min=4, max=25)])
    email = StringField(
        "Email Address", [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField("Password", [
        validators.DataRequired(),
        validators.EqualTo("confirm", message="Passwords must match!")
    ])
    confirm = PasswordField("Confirm Password")
    # accept_tos = BooleanField("I accept the TOS", [validators.DataRequired()])


class LoginForm(Form):
    email = StringField(
        "Email Address", [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField("Password", [validators.DataRequired()])
