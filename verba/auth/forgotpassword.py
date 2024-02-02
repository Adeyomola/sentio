from verba.db import get_db
from verba.metadata import metadata
from flask import request, session, render_template, flash, redirect, Blueprint, g, url_for, send_file
from sqlalchemy.sql import update, delete, select
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from verba.auth.auth import login_required
import os
import pyotp
from verba.auth.email_auth import send_email

bp = Blueprint('forgotpassword', __name__, template_folder='templates', static_folder='static', static_url_path='/auth/static')
md = metadata()
table = md.tables['users']
secret = os.environ.get('TOTP_SECRET')
totp = pyotp.TOTP(secret, interval=60)

@bp.route('/forgotpassword',  methods=['GET', 'POST'], strict_slashes = False)
def forgotpassword():
    if g.user is not None:
        return redirect('/')
    if request.method == 'POST':
        if 'forgotpassword' in request.form:
            error = None
            connection = get_db()
            email = request.form['email']

            statement = select(table).where(table.c.email == email)
            user = connection.execute(statement)
            user = Result.fetchone(user)
        
            if user is None:
                error = "This email is not registered to an account"
                flash(error)
            elif email in user:
                send_email(email, totp.now(), user[1])
                session['unverified_email'] = email
                session['firstname'] = user[1]
                return render_template('verify.html')
        
        if 'submitotp' in request.form:
            otp = request.form['otp']

            if totp.verify(otp):
                return render_template('passwordreset.html')
            else:
                error="Invalid Code"
                flash(error)
                return render_template('verify.html')
            
        if 'resetpassword' in request.form:
            error = None
            connection = get_db()

            password = request.form['password']
            confirm_password=request.form['confirm_password']

            if not password:
                error = "Password required"
            elif not confirm_password:
                error = "Enter your password again"
            if password != confirm_password:
                error = "Passwords do not match"
            
            if error is None:
                statement = statement = (update(table).where(table.c.email == session.get('unverified_email')).values(password=generate_password_hash(password)))
                connection.execute(statement)
                connection.commit()
                connection.close()
                session.clear()
                return redirect('/login')

    return render_template('forgotpassword.html')
		