from verba.db import get_db
from flask import request, session, render_template, flash, redirect, Blueprint, g, url_for, send_file
from sqlalchemy.sql import update
from sqlalchemy.engine import ResultProxy
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from verba.auth.auth import login_required

sqlsession = Session(get_db()[0])
bp = Blueprint('profile', __name__, url_prefix='/profile', template_folder='templates', static_folder='static', static_url_path='/auth/static')
engine = get_db()[0]
md = get_db()[1]


@bp.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    if request.method == 'POST':
        error = None
        connection = engine.connect()
        password = request.form['password']
        confirm_password=request.form['confirm_password']
        table = md.tables['users']

        if not password:
            error = "Password required"
        elif not confirm_password:
            error = "Enter your password again"
        elif password != confirm_password:
            error = "Passwords do not match"
        if error is None:
            statement = (update(table).where(table.c.id == g.get('user')[0]).values(password=generate_password_hash(password)))
            connection.execute(statement)
            connection.commit()
            return redirect("/")
        connection.close()
        flash(error)
    return render_template('changepassword.html')