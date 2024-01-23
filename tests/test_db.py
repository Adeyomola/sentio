import sqlite3
import pytest
from verba.db import get_db, init_db, close_db
from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError


def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()



