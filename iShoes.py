import datetime
import os
import hashlib
from decimal import Decimal
from datetime import date

from flask import Flask, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo, Email

import mysql.connector
from mysql.connector import errorcode

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


class CheckoutForm(FlaskForm):
    first_name = StringField(label='First Name', validators=[DataRequired(message='*Required'), Length(min=3, max=45)])
    last_name = StringField(label='Last Name', validators=[DataRequired(message='*Required'), Length(min=3, max=45)])
    address = StringField(label='Street Address', validators=[DataRequired(message='*Required'),
                                                  Length(min=3, max=100)])
    city = StringField(label='City', validators=[DataRequired(message='*Required'), Length(min=3, max=45)])
    state = StringField(label='State', validators=[DataRequired(message='*Required'), Length(min=2, max=2)])
    zip_code = StringField(label='Zip Code', validators=[DataRequired(message='*Required'),
                                             Length(min=5, max=5, message='Zip Code must be 5 digits')])
    card_number = StringField(label='Card Number', validators=[DataRequired(message='*Required'),
                                                   Length(min=16, max=16, message="Invalid Credit Card Number")])
    card_exp = StringField(label='Exp Date', validators=[DataRequired(message='*Required'), Length(min=5, max=5)])
    card_sec = StringField(label='Security Code', validators=[DataRequired(message='*Required'), Length(min=3, max=3)])

    submit = SubmitField(label='Submit Order')

    def validate_card_number(self, card_number):
        valid_numbers = '0123456789'
        for i in card_number.data:
            if i not in valid_numbers:
                raise ValidationError(f'{card_number.data} is not a valid card number.')

    def validate_card_exp(self, card_exp):
        valid_months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        if card_exp.data[:1] not in valid_months:
            raise ValidationError(f'{card_exp.data[:1]} is not a valid month.')
        if card_exp.data[2] != '/':
            raise ValidationError('Place a slash in between the month and year (i.e. \'04/28\')')
        if not card_exp.data[3:] > '21':
            raise ValidationError(f'Card expired in {card_exp.data[3:]}, please use a valid card.')

    def validate_card_sec(self, card_sec):
        valid_numbers = '0123456789'
        for i in card_sec.data:
            if i not in valid_numbers:
                raise ValidationError(f'{card_sec.data} is not a valid security code.')


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
            return render_template('shop_id.html', username=session['username'], cart_count=session['cart_count'],
                                   item_id=item_id, shoe_brand=data[1], shoe_model=data[2], added_to_cart=True)

    return render_template('shop_id.html', username=session['username'], cart_count=session['cart_count'],
                           item_id=item_id, shoe_brand=data[1], shoe_model=data[2])


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'cart' in session:
        session['total'] = Decimal(0.00)
        for i in session['cart']:
            session['total'] += Decimal(i[4])
        if request.method == 'POST':
            session['cart'].pop(int(request.form.get('remove')))
            session['cart_count'] -= 1
            return redirect(url_for('cart'))
        return render_template('cart.html', username=session['username'], cart_count=session['cart_count'],
                               cart=session['cart'], total=session['total'])
    return render_template('cart.html', username=session['username'], cart_count=session['cart_count'])


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if request.method == 'POST':
        items = []
        cursor = cnx.cursor()

        for i in session['cart']:
            cursor.execute('SELECT shoeID FROM shoes WHERE shoeBrand = %s AND shoeModel = %s '
                           'AND shoeColor = %s AND shoeSize = %s', [i[0], i[1], i[2], i[3]])
            items.append(cursor.fetchone())
        items = [x[0] for x in items]
        items = ' '.join(str(x) for x in items)

        if session['username'] != 'Guest':
            cursor.execute('SELECT userID FROM users WHERE userName = %s', [session['username']])
            user_id = cursor.fetchone()[0]
        else:
            user_id = 0
            
        cur_date = date.today()
        cur_date = cur_date.strftime("%Y-%m-%d")
        cursor.execute('INSERT into orders (userID, orderItems, creditCardNum, creditCardExp, creditCardSec,'
                       'orderDate, total)'
                       'values (%s, %s, %s, %s, %s, %s, %s)',
                       [user_id, items, form.card_number.data, form.card_exp.data, form.card_sec.data, cur_date,
                        session['total']])
        cnx.commit()
        return redirect(url_for('order'))

    if session['username'] != 'Guest':
        cursor = cnx.cursor()
        cursor.execute('SELECT * from users WHERE userName = %s', [session['username']])
        data = cursor.fetchone()

        form.first_name.data = data[3]
        form.last_name.data = data[4]
        form.address.data = data[6]
        form.city.data = data[7]
        form.state.data = data[8]
        form.zip_code.data = data[9]
        return render_template('checkout.html', username=session['username'], cart_count=session['cart_count'],
                               total=session['total'], form=form, logged_in=True)
    return render_template('checkout.html', username=session['username'], cart_count=session['cart_count'],
                           total=session['total'], form=form, logged_in=False)


@app.route('/order')
def order():
    return redirect(url_for('account'))


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

    orders = []
    cursor = cnx.cursor()
    cursor.execute('SELECT userID FROM users WHERE username = %s', [username])
    data = cursor.fetchone()[0]
    cursor.execute('SELECT * FROM orders WHERE userID = %s', [data])
    data = cursor.fetchall()
    for i in data:
        orders.append([i[0], i[6], i[7]])

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


if __name__ == '__main__':
    app.run()
