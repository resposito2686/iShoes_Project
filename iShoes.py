import os
import hashlib
from decimal import Decimal

from flask import Flask, render_template, redirect, url_for, session, request

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
                raise ValidationError(f'Incorrect password for {username.data}')
        else:
            raise ValidationError(f'User Name {username.data} does not exist.')


class CreateAccountForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired(message='*Required'), Length(min=3, max=45)])
    password = PasswordField(label='Password', validators=[DataRequired(message='*Required')])
    confirm = PasswordField(label='Confirm Password', validators=[DataRequired(message='*Required'),
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
                raise ValidationError(f'Error at {i}, User Name cannot contain symbols.')

        cursor = cnx.cursor()
        cursor.execute('SELECT * from users WHERE userName = %s', [username.data])
        data = cursor.fetchone()
        if data is not None:
            raise ValidationError(f'{username.data} is already taken, please choose another.')

    def validate_state(self, state):
        valid_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA",
                        "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM",
                        "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA",
                        "WV", "WI", "WY"]
        if state.data not in valid_states:
            raise ValidationError(f'{state.data} is not a valid state.')


app = Flask(__name__)
app.secret_key = '11b8514a4f71eb68bf34a3a0'
image_folder = os.path.join('static', 'images')

#: MySQL connection
try:
    cnx = mysql.connector.connect(user='root', password='zxcASDqwe1@3', host='localhost', database='ishoesdb')
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


@app.route('/shop/')
def shop():
    return render_template('shop.html', username=session['username'], cart_count=session['cart_count'])


@app.route('/shop/<item_id>', methods=['GET', 'POST'])
def shop_id(item_id):
    cursor = cnx.cursor(buffered=True)
    cursor.execute('SELECT * FROM shoes WHERE modelID = %s', [item_id])
    data = cursor.fetchone()
    cursor.close()

    if request.method == 'POST':
        if 'color' in request.form:
            session['color_choice'] = request.form['color']
            return render_template('shop_id.html', username=session['username'], cart_count=session['cart_count'],
                                   item_id=item_id, shoe_brand=data[1], shoe_model=data[2],
                                   color_choice=session['color_choice'])
        else:
            session['cart_count'] += 1
            if 'cart' not in session:
                session['cart'] = []
            session['cart'].append([data[1], data[2], session['color_choice'], request.form['size'], data[5]])
            session.pop('color_choice')
            print(session['cart'])
            return render_template('shop_id.html', username=session['username'], cart_count=session['cart_count'],
                                   item_id=item_id, shoe_brand=data[1], shoe_model=data[2], added_to_cart=True)

    return render_template('shop_id.html', username=session['username'], cart_count=session['cart_count'],
                           item_id=item_id, shoe_brand=data[1], shoe_model=data[2])


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'cart' in session:
        total = Decimal(0.00)
        for i in session['cart']:
            total += Decimal(i[4])
        if request.method == 'POST':
            session['cart'].pop(int(request.form.get('remove')))
            session['cart_count'] -= 1
            return redirect(url_for('cart'))
        return render_template('cart.html', username=session['username'], cart_count=session['cart_count'],
                               cart=session['cart'], total=total)
    return render_template('cart.html', username=session['username'], cart_count=session['cart_count'])


@app.route('/checkout')
def checkout():
    return render_template('checkout.html', username=session['username'], cart_count=session['cart_count'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('account'))
    return render_template('login.html', username=session['username'], cart_count=session['cart_count'], form=form)


@app.route('/account/')
def account():
    return redirect(url_for('user_account', username=session['username']))


@app.route('/account/<username>')
def user_account(username):
    if session['username'] == 'Guest':
        return redirect(url_for('login'))

    # PLACEHOLDER
    orders = [['000001', 'Complete', '10/19/21', '$126.74'], ['000005', 'Complete', '10/25/21', '$21.77'],
              ['000012', 'Complete', '10/31/21', '$74.65'], ['000025', 'Shipped', '11/04/21', '$22.32']]

    return render_template('account.html', username=username, cart_count=session['cart_count'], orders=orders)


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
        return redirect(url_for('account', username=session['username']))
    return render_template('create_account.html', username=session['username'], cart_count=session['cart_count'],
                           form=form)


@app.route('/logout')
def logout():
    session['username'] = 'Guest'
    return redirect(url_for('home'))


'''
@app.route('/data')
def data():

    shoe_colors = ['red', 'blue', 'black', 'orange', 'white']
    for i in shoe_colors:
        x = 5
        while (x != 13):
            cursor = cnx.cursor()
            cursor.execute('INSERT into shoes '
                           '(shoeBrand, shoeModel, shoeColor, shoeSize, shoePrice, stock) '
                           'values (%s, %s, %s, %s, %s, %s)',
                           ['Nike Sneakers', 'Custom Air Force 1', i, x, 150.00, 3])
            cnx.commit()
            x += 1
    return '<p> DONE </p>'
'''

if __name__ == '__main__':
    app.run()
