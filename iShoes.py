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
    logo_path = os.path.join(image_folder, 'logo.jpg')
    cart_empty_path = os.path.join(image_folder, 'cart_empty.jpg')
    return render_template("home.html", logo_img=logo_path, cart_empty_img=cart_empty_path)


if __name__ == '__main__':
    app.run()
