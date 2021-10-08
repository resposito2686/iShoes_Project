from flask import Flask
from flask import render_template, redirect, url_for
import os

app = Flask(__name__)
image_folder = os.path.join('static', 'images')


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    cart_empty_path = os.path.join(image_folder, 'cart_empty.jpg')
    user_name = "Login"
    return render_template("home.html", cart_empty_img=cart_empty_path, user_name=user_name)


if __name__ == '__main__':
    app.run()
