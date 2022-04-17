from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


# db = SQLAlchemy()
DB_NAME = "liquor_store"

app = Flask(__name__)
app.config["SECRET_KEY"] = "python_ecommerce_demo"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://root:@localhost:3306/{DB_NAME}"
# db.init_app(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)