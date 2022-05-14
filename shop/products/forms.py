from flask_wtf.file import FileAllowed, FileField
from wtforms import Form, IntegerField, DecimalField, StringField, TextAreaField, validators

class ProductForm(Form):
    name = StringField("Name", [validators.DataRequired()])
    origins = StringField("Country of Origins", [validators.DataRequired()])
    price = DecimalField("Price", [validators.DataRequired()])
    discount = IntegerField("Discount", default=0)
    stock = IntegerField("Stock", [validators.DataRequired()])
    description = TextAreaField("Description", [validators.DataRequired()])
    image = FileField("Image", validators=[FileAllowed(["jpg", "jpeg", "png"])])