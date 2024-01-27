from verba.db import get_db
from verba.metadata import metadata
from flask import request, session, render_template, flash, redirect, Blueprint, g, url_for, send_file
from sqlalchemy.sql import update, insert
from sqlalchemy.engine import ResultProxy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from verba.auth.auth import login_required
import re
from verba.blog.uploads import Upload

bp = Blueprint('profile', __name__, template_folder='templates', static_folder='static', static_url_path='/auth/static')
md = metadata()


@bp.route('/profile',  methods=['GET', 'POST'], strict_slashes = False)
@login_required
def profile():
	if request.method == 'POST':
		if 'uploadProfilePicture' in request.form:
			error = None
			connection = get_db()
			table = md.tables['users']
			image_url = Upload.upload_file(Upload)
			if error is None:
				try:
					statement = (update(table).where(table.c.id == g.get('user')[0]).values(image_url=image_url))
					connection.execute(statement)
					connection.commit()
					error = "Your profile picture has been uploaded"
					session['profile_picture'] = image_url
					redirect(url_for('profile.profile'))
				finally:
					connection.close()
			flash(error)
		if 'changepassword' in request.form:
			error = None
			connection = get_db()

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
				try:
					statement = (update(table).where(table.c.id == g.get('user')[0]).values(password=generate_password_hash(password)))
					connection.execute(statement)
					connection.commit()
					error = "Your password has been updated"
				finally:
					connection.close()
			flash(error)

		if 'changedetails' in request.form:
			error = None
			connection = get_db()

			username = request.form['username']
			firstname = request.form['firstname']
			email = request.form['email']
			confirm_email = request.form['confirm_email']
			lastname = request.form['lastname']
			table = md.tables['users']

			if email != confirm_email:
				error = "Email addresses do not match"
				
			if error is None:
				try:
					statement = (update(table).where(table.c.id == g.get('user')[0]).values(username=username, firstname=firstname, lastname=lastname, email=email))
					connection.execute(statement)
					connection.commit()
					error = "Your details have been updated"
					session['firstname'] = firstname
					redirect(url_for('profile.profile'))
				except IntegrityError as ie:
					error = ie._message()
					connection.rollback()
					if re.search('username', error):
						error = 'username has already been taken'
					flash(error)
				finally:
					connection.close()
			flash(error)
	username=g.get('user')[3]
	firstname=g.get('user')[1]
	lastname=g.get('user')[2]
	email=g.get('user')[5]
	return render_template('profile.html', username=username, firstname=firstname, lastname=lastname, email=email)
		