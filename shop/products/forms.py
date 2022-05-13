from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, TextAreaField, validators

class ProductForm(Form):
    name = StringField("Name", [validators.DataRequired()])
    origins = StringField("Country of Origins", [validators.DataRequired()])
    price = IntegerField("Price", [validators.DataRequired()])
    discount = IntegerField("Discount", default=0)
    stock = IntegerField("Stock", [validators.DataRequired()])
    description = TextAreaField("Description", [validators.DataRequired()])
    image = FileField("Image", validators=[FileAllowed(["jpg", "jpeg", "png"])])