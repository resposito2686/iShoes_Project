import os
import hashlib

from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import session

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo, Email

from flask_mysqldb import MySQL


class CreateAccountForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired(message='*Required'), Length(min=3, max=45)])
    password = PasswordField(label='Password', validators=[DataRequired(message='*Required')])
    confirm = PasswordField(label='Confirm Password',
                            validators=[DataRequired(message='*Required'),
                                        EqualTo('password', message='Password must match.')])
    email_address = StringField(label='Email Address',
                                validators=[DataRequired(message='*Required'), Email(), Length(min=3, max=100)])
    first_name = StringField(label='First Name', validators=[DataRequired(message='*Required'), Length(min=3, max=45)])
    last_name = StringField(label='Last Name', validators=[DataRequired(message='*Required'), Length(min=3, max=45)])
    address = StringField(label='Street Address', validators=[DataRequired(message='*Required'),
                                                              Length(min=3, max=100)])
    city = StringField(label='City', validators=[DataRequired(message='*Required'), Length(min=3, max=45)])
    state = StringField(label='State', validators=[DataRequired(message='*Required'), Length(min=2, max=2)])
    zip_code = StringField(label='Zip Code', validators=[DataRequired(message='*Required'),
                                                         Length(min=5, max=5, message='Zip Code must be 5 digits')])

    submit = SubmitField(label='Create')

    def validate_username(self, username):
        illegal_chars = '!@#$%^&*()+={[}]|\\:;\"\'<,>.?/~`'
        for i in username.data:
            if i in illegal_chars:
                raise ValidationError(f'Error at { i }, User Name cannot contain symbols.')

    def validate_state(self, state):
        valid_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA",
                        "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM",
                        "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA",
                        "WV", "WI", "WY"]
        for i in state.data:
            if i in valid_states:
                return True
        raise ValidationError(f'{ state.data } is not a valid state.')


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
    session['cart_count'] = 0
    return redirect(url_for('home'))


@app.route('/home')
def home():
    if 'username' not in session:
        session['username'] = 'Guest'

    return render_template('home.html', username=session['username'], cart_count=session['cart_count'])


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    return render_template('shop.html', username=session['username'], cart_count=session['cart_count'])


@app.route('/cart')
def cart():
    return render_template('cart.html', username=session['username'], cart_count=session['cart_count'])


@app.route('/add_cart')
def add_cart():
    session['cart_count'] += 1
    return redirect(url_for('shop'))


@app.route('/remove_cart')
def remove_cart():
    if session['cart_count'] > 0:
        session['cart_count'] -= 1
    return redirect(url_for('cart'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['userNameInput']

        #:  Password is ran through SHA512 hashing algorithm for security
        password = hashlib.sha512(request.form['passwordInput'].encode('utf-8')).hexdigest()

        #:  EXAMPLE MySQL QUERY
        #:  Please see the 'create_account' function for more detail.
        cursor = mysql.connection.cursor()  # <-- CURSOR FOR QUERIES
        cursor.execute('SELECT * from users WHERE userName = %s', [username])  # <-- QUERY GOES HERE
        sql_data = cursor.fetchone()  # <-- DATA RETURNED AS TUPLE
        print(sql_data)

        if sql_data is not None:
            if sql_data[2] == password:
                session['username'] = username
                return redirect(url_for('home'))
            else:
                error = 'password'
        else:
            error = 'user'
    return render_template('login.html', username=session['username'], cart_count=session['cart_count'], error=error)


@app.route('/account')
def account():
    return render_template('account.html', username=session['username'], cart_count=session['cart_count'])


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():

    form = CreateAccountForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('account'))
    return render_template('create_account.html', username=session['username'], cart_count=session['cart_count'],
                           form=form)
    '''
    password_match = True
    user_match = False

    
    if request.method == 'POST':
        
        username = request.form['userNameInput']
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
    '''
    #:  execute() function arguments are ('''MySQL Query''', (Python variables and literals))
    '''
            cursor.execute('SELECT * from users WHERE userName = %s', [username])

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
                               [username, password, first_name, last_name, email_address, address, city, state,
                                zip_code])

                #:  commit table changes to the MySQL database
                mysql.connection.commit()

                session['username'] = username
                return redirect(url_for('account'))
            else:
                user_match = True

        #:  except block to print any connection errors that may occur.
        except Exception as e:
            print('Error insert data in table...' + str(e))

    return render_template('create_account.html', username=session['username'], cart_count=session['cart_count'],
                           user_match=user_match, password_match=password_match)
    '''


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
