import os
import hashlib

from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import session

from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = '11b8514a4f71eb68bf34a3a0'
image_folder = os.path.join('static', 'images')
cart_empty = True

#:  TODO - install flask_mysqldb by typing 'pip install flask_mysqldb' in your command prompt
#:  DATABASE IP ADDRESS
app.config['MYSQL_HOST'] = 'localhost'

#:  DATABASE USER NAME
app.config['MYSQL_USER'] = 'root'

#:  DATABASE PASSWORD
app.config['MYSQL_PASSWORD'] = 'password123'

#:  SCHEMA NAME
app.config['MYSQL_DB'] = 'ishoesdb'

mysql = MySQL(app)
if mysql:
    print('Connection Successful!')
else:
    print('Connection Failed!')


@app.route('/')
def index():
    session.clear()
    return redirect(url_for('home'))


@app.route('/home')
def home():
    global cart_empty

    cart_empty = True
    if 'user_name' not in session:
        session['user_name'] = 'Guest'

    return render_template('home.html', cart_empty=cart_empty, user_name=session['user_name'])


@app.route('/shop')
def shop():
    global cart_empty

    cart_empty = True
    return render_template('shop.html', user_name=session['user_name'], cart_empty=cart_empty)


@app.route('/cart')
def cart():
    global cart_empty

    cart_empty = False
    return render_template('cart.html', user_name=session['user_name'], cart_empty=cart_empty)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global cart_empty

    error = None
    cart_empty = True

    if request.method == 'POST':
        user_name = request.form['userNameInput']

        #:  Password is ran through SHA512 hashing algorithm for security
        password = hashlib.sha512(request.form['passwordInput'].encode('utf-8')).hexdigest()

        #:  EXAMPLE MySQL QUERY
        #:  Please see the 'create_account' function for more detail.
        cursor = mysql.connection.cursor()                                      # <-- CURSOR FOR QUERIES
        cursor.execute('SELECT * from users WHERE userName = %s', [user_name])  # <-- QUERY GOES HERE
        sql_data = cursor.fetchone()                                            # <-- DATA RETURNED AS TUPLE
        print(sql_data)

        if sql_data is not None:
            if sql_data[2] == password:
                session['user_name'] = user_name
                return redirect(url_for('home'))
            else:
                error = 'password'
        else:
            error = 'user'
    return render_template('login.html', user_name=session['user_name'], error=error, cart_empty=cart_empty)


@app.route('/account')
def account():
    global cart_empty

    cart_empty = False
    return render_template('account.html', user_name=session['user_name'])


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    global cart_empty

    cart_empty = True
    password_match = True
    user_match = False

    if request.method == 'POST':
        user_name = request.form['userNameInput']
        password = hashlib.sha512(request.form['passwordInput'].encode('utf-8')).hexdigest()
        password_ver = hashlib.sha512(request.form['passwordInputVer'].encode('utf-8')).hexdigest()
        if password != password_ver:
            password_match = False
        email_address = request.form['emailAddress']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zipCode']

        #:  --- How to insert data into a MySQL database ---
        #:  try block to catch any connection errors that could result in a crash
        try:
            #:  cursor used to execute commands
            cursor = mysql.connection.cursor()

            #:  execute() function arguments are ('''MySQL Query''', (Python variables and literals))
            cursor.execute('SELECT * from users WHERE userName = %s', [user_name])

            #: The query data is fetched and stored in the variable 'data'
            data = cursor.fetchone()
            print(data)

            if data is None:

                #:  values being placed into a table are ALWAYS %s, which is placeholder that will be filled by the
                #   Python variables and literals in the function argument.
                #:
                #:  Python variables and literals are a List with data indexed in the same order it appears in the
                #   MySQL query.
                cursor.execute('INSERT into users '
                               '(userName, password, firstName, lastName, emailAddress, address, city, state, zipCode) '
                               'values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                               [user_name, password, first_name, last_name, email_address, address, city, state,
                                zip_code])

                #:  commit table changes to the MySQL database
                mysql.connection.commit()

                session['user_name'] = user_name
                return redirect(url_for('account'))
            else:
                user_match = True

        #:  except block to print any connection errors that may occur.
        except Exception as e:
            print('Error insert data in table...' + str(e))

    return render_template('create_account.html', user_name=session['user_name'], user_match=user_match,
                           password_match=password_match, cart_empty=cart_empty)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
