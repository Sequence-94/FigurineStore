from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager


app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config['SECRET_KEY'] = 'd4d2ac62ad021343b05f57dd'
# create the extension
db = SQLAlchemy(app)
Bootstrap5(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
with app.app_context():
    db.create_all()

# hash passwords
bcrypt = Bcrypt(app)

from shop import routes