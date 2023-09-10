from shop import app
from flask import render_template, redirect, url_for, flash, request
from shop.models import Item, User, Cart
from shop.forms import RegisterForm, LoginForm, PurchaseForm, CartForm, RemoveCartForm
from shop import db
from flask_login import login_user, logout_user, login_required, current_user
import stripe
from os import *

import os
stripe.api_key = "sk_test_51NoAqSGloACtem36BSZdAYPyEwfkeh6CwN1DSRQddp1RGQTZ8IbU5NM2lY3nj1oXnti21jeVfndBY0QXg8cVl2DI00Du37g3R9"


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/shop", methods=['GET', 'POST'])
@login_required
def shop_page():
    cart_form = CartForm()
    if cart_form.validate_on_submit():
        item_to_cart = request.form.get('carted_item')
        c_item_object = Item.query.filter_by(name=item_to_cart).first()
        if c_item_object:
            new_cart = Cart(
                customer_id=current_user.id,
                item_id=c_item_object.id
            )
            db.session.add(new_cart)
            db.session.commit()
    items = Item.query.all()
    return render_template('shop.html', items=items, cart_form=cart_form)


@app.route("/cart", methods=['GET', 'POST'])
def cart_page():
    remove_cart_form = RemoveCartForm()
    if remove_cart_form.validate_on_submit():
        item_to_remove = request.form.get('remove_item')

        Cart.query.filter_by(item_id=item_to_remove).delete()
        db.session.commit()
        return redirect(url_for('cart_page'))

    total = 0
    carts = Cart.query.filter_by(customer_id=current_user.id).all()
    current_user_cart = [Item.query.filter_by(id=cart.item_id).first() for cart in carts]
    for item in current_user_cart:
        total += item.price

    return render_template('cart.html', current_user_cart=current_user_cart, total=total,
                           remove_cart_form=remove_cart_form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correct(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(message=f'Success! You are logged in as: {attempted_user.username}', category='scuccess')
            return redirect(url_for('shop_page'))
        else:
            flash(message='Username and password do not match! Please try agan', category='danger')

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print(form.validate())
        print(form.errors)
        new_user = User(
            username=form.username.data,
            email=form.email_address.data,
            password_hash=form.password1.data
            # password_hash
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'Account created successfully! Logged in as {new_user.username}', category='success')

        return redirect(url_for('shop_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error creating the user: {err_msg}', category='danger')
    return render_template("register.html", form=form)


@app.route("/create-checkout-session", methods=['GET', 'POST'])
def create_checkout_session():
    customer_items = []
    input_string = request.form.get('products')
    # Split the string into individual items and remove "<Item " and ">"
    items = input_string.split(', ')
    customer_products = [int(item.replace('<Item ', '').replace('>', '').replace('[', '').replace(']', '')) for item in
                         items]

    for product_id in customer_products:
        print(f"product id:{product_id}")
        print(f"name of product:{Item.query.filter_by(id=product_id).first().name}")
        stripe_product_id = stripe.Product.create(
            name=Item.query.filter_by(id=product_id).first().name,
            # description=Item.query.filter_by(id=customer_products[product_id]).first().description,
            # images=Item.query.filter_by(id=customer_products[product_id]).first().image_url
        ).id
        print(f"product id:{stripe_product_id}")
        price_id = stripe.Price.create(
            unit_amount=int(Item.query.filter_by(id=product_id).first().price)*100,
            currency="zar",
            product=stripe_product_id,
        ).id
        print(f"price id:{price_id}")
        new_item = {
            "price": price_id,
            "quantity": 1
        }
        customer_items.append(new_item)
        print(f"customer items:{customer_items}")

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=customer_items,
            mode='payment',
            success_url=render_template("success.html"),
            cancel_url=render_template("cancel.html"),
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/cancel")
def cancel():
    return render_template("cancel.html")


@app.route("/success")
def success():
    return render_template("success.html")
