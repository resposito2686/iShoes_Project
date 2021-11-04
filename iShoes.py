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


class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired(message='*Required'), Length(min=3, max=45)])
    password = PasswordField(label='Password', validators=[DataRequired(message='*Required')])
    login = SubmitField(label='Login')

    def validate_username(self, username):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * from users WHERE userName = %s', [username.data])
        data = cursor.fetchone()

        if data is not None:
            if data[2] == self.password.data:
                session['username'] = username.data
                return True
            else:
                raise ValidationError(f'Incorrect password for { username.data }')
        else:
            raise ValidationError(f'User Name { username.data } does not exist.')


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

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * from users WHERE userName = %s', [username.data])
        data = cursor.fetchone()
        print(data)
        if data is not None:
            raise ValidationError(f'{ username.data } is already taken, please choose another.')


    def validate_state(self, state):
        valid_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA",
                        "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM",
                        "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA",
                        "WV", "WI", "WY"]
        if state.data in valid_states:
            return True
        raise ValidationError(f'{ state.data } is not a valid state.')


app = Flask(__name__)
app.secret_key = '11b8514a4f71eb68bf34a3a0'
image_folder = os.path.join('static', 'images')

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
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('account'))
    return render_template('login.html', username=session['username'], cart_count=session['cart_count'])


@app.route('/account')
def account():
    return render_template('account.html', username=session['username'], cart_count=session['cart_count'])


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form = CreateAccountForm()
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT into users '
                       '(userName, password, firstName, lastName, emailAddress, address, city, state, zipCode) '
                       'values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       [form.username.data, form.password.data, form.first_name.data, form.last_name.data,
                        form.email_address.data, form.address.data, form.city.data, form.state.data,
                        form.zip_code.data])
        mysql.connection.commit()
        session['username'] = form.username.data
        mysql.connection.commit()
        return redirect(url_for('account'))
    return render_template('create_account.html', username=session['username'], cart_count=session['cart_count'],
                           form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
