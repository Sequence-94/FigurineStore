from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
import os

app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config['SECRET_KEY'] = 'd4d2ac62ad021343b05f57dd'
app.config['STRIPE_PUBLIC_KEY'] = "pk_test_51NoAqSGloACtem36CS01mEX1b3odSPEKjX05Zw0ab7daOWkIfBu98O27YCvuPcGYmwRIuIqtxTrTizw2pW9gQ4Fa00uwy0stSF"
app.config['STRIPE_SECRET_KEY'] = "sk_test_51NoAqSGloACtem36BSZdAYPyEwfkeh6CwN1DSRQddp1RGQTZ8IbU5NM2lY3nj1oXnti21jeVfndBY0QXg8cVl2DI00Du37g3R9"
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