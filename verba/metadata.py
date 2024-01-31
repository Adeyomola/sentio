from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, Text, ForeignKey, NVARCHAR, Boolean
import datetime

def metadata():
    md = MetaData()

    users = Table(
    'users', md, 
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('firstname', String(255)),
    Column('lastname', String(255)),
    Column('username', String(255), unique=True),
    Column('password', String(255)),
    Column('email', String(255), unique=True),
    Column('image_url', NVARCHAR),
    Column('isVerified', Boolean, default=False)
        )
    post = Table(
    'post', md,
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('author_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('firstname', String(255)),
    Column('created', TIMESTAMP, default=datetime.datetime.utcnow),
    Column('title', Text, nullable=False),
    Column('body', Text, nullable=False),
    Column('image_url', NVARCHAR)
    )
    return md