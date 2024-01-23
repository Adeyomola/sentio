import datetime
from flask import current_app, g
import sqlalchemy
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, Text, ForeignKey
import os
from dotenv import load_dotenv
load_dotenv()

db_password=os.environ.get('DB_PASSWORD')
db_user=os.environ.get('DB_USER')
host=os.environ.get('HOST')
db_name=os.environ.get('DATABASE')
dbms="mysql"

def metadata(dbms):
    if dbms == "sqlite3":
        engine = sqlalchemy.create_engine(f"{dbms}:///{db_name}")
    else:
        engine = sqlalchemy.create_engine(f"{dbms}://{db_user}:{db_password}@{host}/{db_name}")

    md = MetaData()

    users = Table(
    'users', md, 
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('firstname', String(255)),
    Column('lastname', String(255)),
    Column('username', String(255), unique=True),
    Column('password', String(255)),
    Column('email', String(255), unique=True),
        )
    post = Table(
    'post', md,
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('author_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('firstname', String(255)),
    Column('created', TIMESTAMP, default=datetime.datetime.utcnow),
    Column('title', Text, nullable=False),
    Column('body', Text, nullable=False)
    )
    return [engine, md]

def get_db():
    if 'db' not in g:
        if current_app.config['DBMS'] == "sqlite3":
            engine = sqlalchemy.create_engine(f"{current_app.config['DBMS']}:///{db_name}")
            g.db = engine.connect()
        else:
            engine = sqlalchemy.create_engine(f"mysql://{db_user}:{db_password}@{host}/{db_name}")
            g.db = engine.connect()
    return g.db

def init_db():
    engine = metadata(dbms)[0]
    md = metadata(dbms)[1]
    md.create_all(engine)

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

import click
@click.command('db-init')
def db_init():
    init_db()
    click.echo('Database initialized')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(db_init)