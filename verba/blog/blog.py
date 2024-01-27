from verba.db import get_db
from verba.metadata import metadata
from flask import request, render_template, flash, redirect, session, Blueprint, g, url_for
from sqlalchemy import insert, select, delete, update
from sqlalchemy.engine import ResultProxy
from sqlalchemy.exc import IntegrityError
from verba.auth.auth import login_required
import re
from verba.blog.uploads import Upload
from verba.blog.verify import Verify

bp = Blueprint('blog', __name__, template_folder='templates', static_folder='static', static_url_path='/blog/static')

md = metadata()
table = md.tables['post']

def author_posts():
    connection = get_db()
    statement = (select(table).where(table.c.author_id == session['user_id']))
    posts = connection.execute(statement).fetchall()
    connection.close()
    return posts

def front_posts():
    connection = get_db()
    statement = (select(table))
    posts = connection.execute(statement).fetchmany(8)
    connection.close()
    return posts

@bp.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    if request.method == 'POST':
        error = None
        title = request.form['title']
        body = request.form['body']
        connection = get_db()
        image_url = Upload.upload_file(Upload)
        if error is None:
            try:
                statement = (insert(table).values(title=title, author_id=g.get('user')[0], firstname=g.get('user')[1], body=body, image_url=image_url))
                connection.execute(statement)
                connection.commit()
                return redirect('/')
            except IntegrityError as ie:
                error = ie._message()
                connection.rollback()
                if re.search('title', error):
                    error = "An article with this title already exists"
                elif re.search('body', error):
                    error = "This article might be a duplicate"
            finally:
                connection.close()
        flash(error)
    return render_template('write.html')

@bp.route('/post', strict_slashes=False)
def post():
    connection = get_db()
    statement = (select(table))
    posts = connection.execute(statement).fetchall()
    connection.close()
    return render_template('post.html', posts=posts)

@bp.route('/post/<post_id>')
def get_post(post_id):
    connection = get_db()
    Verify.verify_post(post_id, table, connection)
    statement = (select(table).where(table.c.id == post_id))
    post_row = connection.execute(statement)
    post_row = ResultProxy.fetchone(post_row)
    connection.close()
    return render_template('get_post.html', post_row=post_row)

@bp.route('/post/update/<post_id>',  methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    connection = get_db()
    Verify.verify_author(post_id, table, connection)
    post_row = ResultProxy.fetchone(connection.execute(select(table).where(table.c.id == post_id)))
    if request.method == 'POST':
        try:
            if request.files['file']:
                Upload.delete_file(post_row[6])
                image_url = Upload.upload_file(Upload)
            elif post_row[6]:
                image_url = post_row[6]
            else:
                image_url = None
            title = request.form['title']
            body = request.form['body']          
            connection.execute((update(table).where(table.c.id == post_id).values(title=title, body=body, image_url=image_url)))
            connection.commit()
            return redirect(url_for('blog.get_post', post_id=post_row[0]))
        finally:
            connection.close()
    connection.close()
    return render_template('update.html', post_row=post_row)

@bp.route('/post/delete/<post_id>',  methods=['POST'])
@login_required
def delete_post(post_id):
    connection = get_db()
    Verify.verify_author(post_id, table, connection)
    connection.execute((delete(table).where(table.c.id == post_id)))
    connection.commit()
    connection.close()
    return redirect(url_for('blog.post'))