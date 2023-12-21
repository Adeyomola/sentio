from sentio.db import get_db
from flask import request, session, render_template, flash, redirect, Blueprint, g, url_for
from sqlalchemy.sql import select, insert
from sqlalchemy.engine import ResultProxy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash
import re
import functools

sqlsession = Session(get_db()[0])

bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static', static_url_path='/auth/static')
connection = get_db()[1]
md = get_db()[2]


@bp.before_app_request
def current_user():
    table = md.tables['users']
    user_id = session.get('user_id')
    if user_id is None:
        g.user= None
    else:
        g.user = ResultProxy.fetchone(connection.execute(select(table).where(table.c.id == user_id)))

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
        email = request.form['email']
        password = request.form['password']
        table = md.tables['users']
        statement = (
            select(table).where(table.c.email == email)
        )

        rp = ResultProxy
        user = connection.execute(statement)
        user = rp.fetchone(user)

        if user is None:
            error = 'Incorrect email address or password'
        elif not check_password_hash(user[4], password):
            error = 'Incorrect email address or password'
        if error is None:
            session.clear()
            session['user_id'] = user[0]
            session['firstname'] = user[1]
            return redirect("/")
        flash(error)
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None:
        return redirect('/')
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']
        confirm_password=request.form['confirm_password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        table = md.tables['users']

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
            error = "Password does not match"
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
                    flash(error)
                elif re.search('username', error):
                    error = 'username has already been taken'
                    flash(error)
            finally:
                return redirect("/login")
        flash(error)
    return render_template('register.html')
