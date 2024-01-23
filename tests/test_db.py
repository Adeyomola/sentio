import sqlite3
import pytest
from verba.db import get_db, init_db, close_db
from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError

import os
from dotenv import load_dotenv
load_dotenv()

db_name = os.getenv('DATABASE')
dbms="sqlite3"

def test_get_db(app):
    with app.app_context():
        engine = get_db(dbms)[0]
        table = get_db(dbms)[1].tables['post']
        connection = engine.connect()
        assert str(engine) == f'Engine(sqlite:///{db_name})'



