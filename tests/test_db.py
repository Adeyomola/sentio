import sqlite3
import pytest
from verba.db import get_db, init_db, close_db
from verba.metadata import metadata
from sqlalchemy import select
from sqlalchemy.exc import ResourceClosedError


def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
    with  pytest.raises(ResourceClosedError) as e:
        post = metadata().tables['post']
        db.execute((select(post).where(post.c.id == 1)))
    assert 'closed' in str(e.value)



