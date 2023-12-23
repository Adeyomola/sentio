import datetime
import sqlalchemy as db
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, Text, ForeignKey
import os
from dotenv import load_dotenv
load_dotenv()

db_password=os.environ.get('DB_PASSWORD')
db_user=os.environ.get('DB_USER')
host=os.environ.get('HOST')
# host='192.168.56.11'
db_name=os.environ.get('DATABASE')

def get_db():
    engine = db.create_engine(f"mysql://{db_user}:{db_password}@{host}/{db_name}")
    connection = engine.connect()
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

    return [engine, connection, md]

def init_db():
    md = get_db()[2]
    engine = get_db()[0]
    md.create_all(engine)

def close_db(e=None):
    engine = get_db()[0]
    engine.dispose()

import click
@click.command('db-init')
def db_init():
    init_db()
    click.echo('Database initialized')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(db_init)