from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os


# db = SQLAlchemy()
DB_NAME = "liquor_store"

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "python_ecommerce_demo"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://root:@localhost:3306/{DB_NAME}"

photos = UploadSet("photos", IMAGES)

configure_uploads(app, photos)
patch_request_class(app)

# db.init_app(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from shop.admin import routes
from shop.products import routes