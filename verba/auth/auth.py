from verba.db import get_db
from verba.metadata import metadata
from flask import request, session, render_template, flash, redirect, Blueprint, g, url_for
from sqlalchemy.sql import select, insert, update
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
import re
import functools
from verba.auth.email_auth import send_email
import pyotp
import secrets
import base64

bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static', static_url_path='/auth/static')
md = metadata()

totp = pyotp.TOTP(base64.b32encode(secrets.token_hex(5)).decode('utf-8'), interval=300)

@bp.before_app_request
def current_user():
    user_id = session.get('user_id')
    table = md.tables['users']
    connection = get_db()

    if user_id is None:
        g.user = None
    else:
        statement = select(table).where(table.c.id == user_id)
        user = connection.execute(statement)
        user = Result.one(user)
        g.user = user

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None:
        return redirect('/')
    if request.method == 'POST':
        error = None
        connection = get_db()

        email = request.form['email']
        password = request.form['password']
        table = md.tables['users']
        statement = (
            select(table).where(table.c.email == email)
        )
        user = connection.execute(statement)
        user = Result.fetchone(user)

        if user is None:
            error = 'Incorrect email address or password'
        elif not check_password_hash(user[4], password):
            error = 'Incorrect email address or password'
        if error is None:
            try:
                session.clear()
                session['user_id'] = user[0]
                return redirect("/")
            finally:
                connection.close()
        flash(error)
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None:
        return redirect('/')
    if request.method == 'POST':
        if 'register' in request.form:
            error = None
            connection = get_db()
            table = md.tables['users']

            username = request.form['username']
            password = request.form['password']
            confirm_password=request.form['confirm_password']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            
            if not username:
                error = "Username required"
            elif not password:
                error = "Password required"
            elif not confirm_password:
                error = "Enter your password again"
            elif not firstname:
                error = "This field is required"
            elif not lastname:
                error = "This field is required"
            elif not email:
                error = "This field is required"
            if password != confirm_password:
                error = "Passwords do not match"
            if error is None:
                try:
                    statement = (insert(table).values(username=username, password=generate_password_hash(password), firstname=firstname, lastname=lastname, email=email))
                    connection.execute(statement)
                    connection.commit()
                except IntegrityError as ie:
                    error = ie._message()
                    connection.rollback()
                    if re.search('email', error):
                        error = 'account already exists'
                    elif re.search('username', error):
                        error = 'username has already been taken'
                else:
                    send_email(email, totp.now(), firstname)
                    session['unverified_email'] = email
                    session['firstname'] = firstname
                    connection.close()
                    return render_template('verify.html')
        if 'submitotp' in request.form:
            error = None
            otp = request.form['otp']

            if session.get('unverified_email') is None:
                abort(401, f'Unauthorized')

            if totp.verify(otp):
                connection = get_db()
                table = md.tables['users']
                statement = statement = (update(table).where(table.c.email == session.get('unverified_email')).values(isVerified=True))
                connection.execute(statement)
                connection.commit()
                connection.close()
                session.clear()
                return redirect('/login')
            else:
                error="Invalid Code"
                return render_template('verify.html')
        if 'resend' in request.form:
            if session.get('unverified_email') is None:
                abort(401, f'Unauthorized')
            else:
                send_email(session.get('unverified_email'), totp.now(), session.get('firstname'))
                return render_template('verify.html')
        flash(error)
    return render_template('register.html')