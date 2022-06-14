from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_msearch import Search
from flask_login import LoginManager
import os


# db = SQLAlchemy()
DB_NAME = "liquor_store"

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "python_ecommerce_demo"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://root:@localhost:3306/{DB_NAME}"
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(base_dir, "static/images")

photos = UploadSet("photos", IMAGES)

configure_uploads(app, photos)
patch_request_class(app)

# db.init_app(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

search = Search()
search.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "customer_login"
login_manager.needs_refresh_message_category = "danger"
login_manager.login_message = "Please login first!"

from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customers import routes