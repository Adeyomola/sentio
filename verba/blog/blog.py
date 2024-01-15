from verba.db import get_db
from flask import request, render_template, flash, redirect, session, Blueprint, g, url_for
from sqlalchemy import insert, select, delete, update
from sqlalchemy.engine import ResultProxy
from sqlalchemy.exc import IntegrityError
from verba.auth.auth import login_required
from werkzeug.exceptions import abort
import re
from sqlalchemy.orm import Session

sqlsession = Session(get_db()[0])
bp = Blueprint('blog', __name__, template_folder='templates', static_folder='static', static_url_path='/blog/static')
engine = get_db()[0]
md = get_db()[1]
table = md.tables['post']

connection = engine.connect()

class Verify:
    def __init__(self, post_id) -> None:
        self.post_id = post_id

    def verify_author(post_id):
        row = connection.execute((select(table).where(table.c.id == post_id))) 
        row = ResultProxy.fetchone(row)
        if row is None:
            abort(404, f'Post does not exist')
        if not session:
            redirect(url_for('auth.login'))
        elif session['user_id'] != row[1] and session['user_id'] != 1:
            abort(401, f'Unauthorized')
        sqlsession.rollback()
    
    def verify_post(post_id):
        row = connection.execute((select(table).where(table.c.id == post_id))) 
        row = ResultProxy.fetchone(row)
        if row is None:
            abort(404, f'Post does not exist')
        sqlsession.rollback()

def author_posts():
    statement = (select(table).where(table.c.author_id == session['user_id']))
    posts = connection.execute(statement).fetchall()
    sqlsession.close()
    return posts

def front_posts():
    statement = (select(table))
    posts = connection.execute(statement).fetchmany(8)
    sqlsession.close()
    return posts

@bp.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    if request.method == 'POST':
        error = None
        title = request.form['title']
        body = request.form['body']

        if error is None:
            try:
                statement = (insert(table).values(title=title, author_id=g.get('user')[0], firstname=g.get('user')[1], body=body))
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
        flash(error)
        sqlsession.close()
    return render_template('write.html')

@bp.route('/post', strict_slashes=False)
def post():
    statement = (select(table))
    posts = connection.execute(statement).fetchall()
    sqlsession.close()
    return render_template('post.html', posts=posts)

@bp.route('/post/<post_id>')
def get_post(post_id):
    Verify.verify_post(post_id)
    statement = (select(table).where(table.c.id == post_id))
    post_row = connection.execute(statement)
    post_row = ResultProxy.fetchone(post_row)
    sqlsession.close()
    return render_template('get_post.html', post_row=post_row)

@bp.route('/post/update/<post_id>',  methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    Verify.verify_author(post_id)
    table = md.tables['post']
    post_row = ResultProxy.fetchone(connection.execute(select(table).where(table.c.id == post_id)))
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        connection.execute((update(table).where(table.c.id == post_id).values(title=title, body=body)))
        connection.commit()
        return redirect(url_for('blog.get_post', post_id=post_row[0]))
    else:
        sqlsession.close()
        return render_template('update.html', post_row=post_row)

@bp.route('/post/delete/<post_id>',  methods=['POST'])
@login_required
def delete_post(post_id):
    Verify.verify_author(post_id)
    table = md.tables['post']
    connection.execute((delete(table).where(table.c.id == post_id)))
    connection.commit()
    sqlsession.close()
    return redirect(url_for('blog.post'))
    # return redirect(request.referrer)