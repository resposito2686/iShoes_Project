from flask import Flask
from flask import render_template, redirect, url_for, request
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
image_folder = os.path.join('static', 'images')
user_name = 'Login'
active_page = ''
cart_empty = True


# TODO - install flask_mysqldb by typing 'pip install flask_mysqldb' in your command prompt
# DATABASE IP ADDRESS
app.config['MYSQL_HOST'] = 'localhost'

# DATABASE USER NAME
app.config['MYSQL_USER'] = 'root'

# DATABASE PASSWORD
app.config['MYSQL_PASSWORD'] = ''

# SCHEMA NAME
app.config['MYSQL_DB'] = ''

mysql = MySQL(app)
if mysql:
    print("Connection Successful!")
else:
    print('Connection Failed!')


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    global active_page, user_name, cart_empty

    ''' 
    EXAMPLE MySQL QUERY
        cursor = mysql.connection.cursor()    <-- CURSOR FOR QUERIES
        cursor.execute("SELECT * from table") <-- QUERY GOES HERE
        sql_data = cursor.fetchone()          <-- DATA RETURNED AS TUPLE
    '''

    active_page = 'home'
    cart_empty = True
    return render_template("home.html", active=active_page, cart_empty=cart_empty, user_name=user_name)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    global active_page, user_name, cart_empty

    active_page = 'login'
    cart_empty = True

    if request.method == 'POST':
        user_name = request.form['userNameInput']
        password = request.form['passwordInput']
        print(user_name)
        print(password)

    return render_template("login.html", active=active_page, user_name=user_name, cart_empty=cart_empty)


# @app.route('/<user>')
# def user(user):


if __name__ == '__main__':
    app.run()
