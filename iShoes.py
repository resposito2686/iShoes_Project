from flask import Flask
from flask import render_template, redirect, url_for, request
from flask_mysqldb import MySQL
import os
import hashlib

app = Flask(__name__)
image_folder = os.path.join('static', 'images')
user_name = 'Guest'
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
    print("Connection Successful!")
else:
    print('Connection Failed!')


@app.route('/')
def index():
    #:  EXAMPLE MySQL QUERY
    #:    connect = mysql.connect()             <-- CURSOR FOR QUERIES
    #:    cursor.execute("SELECT * from table") <-- QUERY GOES HERE
    #:    sql_data = cursor.fetchone()          <-- DATA RETURNED AS TUPLE

    return redirect(url_for('home'))


@app.route('/home')
def home():
    global user_name, cart_empty

    cart_empty = True
    return render_template("home.html", cart_empty=cart_empty, user_name=user_name)


@app.route('/shop')
def shop():
    global user_name, cart_empty

    cart_empty = True
    return render_template("shop.html", user_name=user_name, cart_empty=cart_empty)


@app.route('/cart')
def cart():
    global user_name, cart_empty

    cart_empty = False
    return render_template("cart.html", user_name=user_name, cart_empty=cart_empty)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_name, cart_empty

    cart_empty = True

    if request.method == 'POST':
        user_name = request.form['userNameInput']

        #:  Password is ran through SHA512 hashing algorithm for security
        password = hashlib.sha512(request.form['passwordInput'].encode('utf-8')).hexdigest()

        #:  --- How to insert data into a MySQL database ---
        #:  try block to catch any connection errors that could result in a crash
        try:
            #:  cursor used to execute commands
            cursor = mysql.connection.cursor()

            #:  execute() function arguments are ("""MySQL Query""", (Python variables and literals))
            #:
            #:  values are ALWAYS %s, which is placeholder value that will be filled by the Python variables
            #:  and literals
            #:
            #:  Python variables and literals are a Tuple with data indexed in the same order it appears in the MySQL
            #:  query.
            cursor.execute("""INSERT into 
                            users (
                                addressCity,
                                addressNum,
                                addressState,
                                addressStreet,
                                addressZip,
                                emailAddress,
                                firstName,
                                lastName,
                                password,
                                phoneNumber,
                                userName)
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                           ('San Diego', '123', 'CA', 'Fake Street', '92115', 'johndoe@gmail.com', 'John', 'Doe',
                            password, '6195555555', user_name))

            #:  commit changes to MySQL database
            mysql.connection.commit()

        #:  except block to print any connection errors that may occur.
        except Exception as e:
            print('Error insert data in table...' + str(e))

    return render_template("login.html", user_name=user_name, cart_empty=cart_empty)


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    global user_name, cart_empty

    cart_empty = True
    password_match = True

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

        print(user_name)
        print(password_match)
        print(email_address)
        print(first_name)
        print(last_name)
        print(address)
        print(city)
        print(state)
        print(zip_code)

    return render_template("create_account.html", user_name=user_name, cart_empty=cart_empty)

# @app.route('/<user>')
# def user(user):


if __name__ == '__main__':
    app.run()
