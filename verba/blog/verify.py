from flask import redirect, session, url_for
from sqlalchemy import select
from sqlalchemy.engine import ResultProxy
from werkzeug.exceptions import abort

class Verify:
    def __init__(self) -> None:
        pass
    
    def verify_author(post_id, table, connection):
        row = connection.execute((select(table).where(table.c.id == post_id))) 
        row = ResultProxy.fetchone(row)
        if row is None:
            abort(404, f'Post does not exist')
        if 'user_id' not in session:
            redirect(url_for('auth.login'))
        elif session['user_id'] != row[1] and session['user_id'] != 1:
            abort(401, f'Unauthorized')
        connection.rollback()
    
    def verify_post(post_id, table, connection):
        row = connection.execute((select(table).where(table.c.id == post_id))) 
        row = ResultProxy.fetchone(row)
        if row is None:
            abort(404, f'Post does not exist')
        connection.rollback()