from flask import Flask
from flask import render_template, redirect, url_for
import os

app = Flask(__name__)
image_folder = os.path.join('static', 'images')
user_name = 'Login'
active_page = ''
cart_empty = True


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    global active_page, user_name, cart_empty

    active_page = 'home'
    cart_empty = True
    return render_template("home.html", active=active_page, user_name=user_name, cart_empty=cart_empty)


@app.route('/shop')
def shop():
    global active_page, user_name, cart_empty

    active_page = 'shop'
    cart_empty = True
    return render_template("shop.html", active=active_page, user_name=user_name, cart_empty=cart_empty)


@app.route('/create')
def create():
    global active_page, user_name, cart_empty

    active_page = 'create'
    cart_empty = False
    return render_template("create.html", active=active_page, user_name=user_name, cart_empty=cart_empty)


@app.route('/login')
def login():
    global active_page, user_name, cart_empty

    active_page = 'login'
    cart_empty = True
    return render_template("login.html", active=active_page, user_name=user_name, cart_empty=cart_empty)


if __name__ == '__main__':
    app.run()
