from flask import Flask
from flask import render_template, redirect, url_for
import os

app = Flask(__name__)
image_folder = os.path.join('static', 'images')
user_name = 'Login'
active_page = ''


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    global active_page, user_name

    active_page = 'home'
    return render_template("home.html", active=active_page, user_name=user_name)


@app.route('/shop')
def shop():
    global active_page, user_name

    active_page = 'shop'
    return render_template("shop.html", active=active_page, user_name=user_name)


@app.route('/create')
def create():
    global active_page, user_name

    active_page = 'create'
    return render_template("create.html", active=active_page, user_name=user_name)


@app.route('/login')
def login():
    global active_page, user_name

    active_page = 'login'
    return render_template("login.html", active=active_page, user_name=user_name)


if __name__ == '__main__':
    app.run()
