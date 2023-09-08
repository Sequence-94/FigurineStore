from shop import db, login_manager
from shop import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    @property
    def password_hash(self):
        return self.password_hash

    @password_hash.setter
    def password_hash(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correct(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

class Cart(db.Model, UserMixin):
    __tablename__ = "carts"
    cart_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))


class Item(db.Model, UserMixin):
    __tablename__ = "items"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Float(), nullable=False)
    description = db.Column(db.String(length=255), nullable=False, unique=True)
    image_url = db.Column(db.String(255), nullable=False, unique=True)
    stock = db.Column(db.Integer(), nullable=False, default=7)





