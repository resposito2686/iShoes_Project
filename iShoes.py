import os
import hashlib

from flask import Flask, render_template, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo, Email

import mysql.connector
from mysql.connector import errorcode


class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired(message='*Required'), Length(min=3, max=45)])
    password = PasswordField(label='Password', validators=[DataRequired(message='*Required')])
    submit = SubmitField(label='Login')

    def validate_username(self, username):
        
        cursor = cnx.cursor()
        cursor.execute('SELECT * from users WHERE userName = %s', [username.data])
        data = cursor.fetchone()

        if data is not None:
            if data[2] == hashlib.sha512(self.password.data.encode('utf-8')).hexdigest():
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

        cursor = cnx.cursor()
        cursor.execute('SELECT * from users WHERE userName = %s', [username.data])
        data = cursor.fetchone()
        if data is not None:
            raise ValidationError(f'{ username.data } is already taken, please choose another.')

    def validate_state(self, state):
        valid_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA",
                        "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM",
                        "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA",
                        "WV", "WI", "WY"]
        if state.data not in valid_states:
            raise ValidationError(f'{ state.data } is not a valid state.')


app = Flask(__name__)
app.secret_key = '11b8514a4f71eb68bf34a3a0'
image_folder = os.path.join('static', 'images')

#: MySQL connection
try:
    cnx = mysql.connector.connect(user='root', password='password123', host='localhost', database='ishoesdb')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("MYSQL ERROR: Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("MYSQL ERROR: Database does not exist.")
    else:
        print(err)


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
    return render_template('login.html', username=session['username'], cart_count=session['cart_count'], form=form)


@app.route('/account')
def account():
    return render_template('account.html', username=session['username'], cart_count=session['cart_count'])


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form = CreateAccountForm()
    if form.validate_on_submit():

        cursor = cnx.cursor()
        cursor.execute('INSERT into users '
                       '(userName, password, firstName, lastName, emailAddress, address, city, state, zipCode) '
                       'values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       [form.username.data, hashlib.sha512(form.password.data.encode('utf-8')).hexdigest(),
                        form.first_name.data, form.last_name.data, form.email_address.data, form.address.data,
                        form.city.data, form.state.data, form.zip_code.data])
        cnx.commit()
        session['username'] = form.username.data
        return redirect(url_for('account'))
    return render_template('create_account.html', username=session['username'], cart_count=session['cart_count'],
                           form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
