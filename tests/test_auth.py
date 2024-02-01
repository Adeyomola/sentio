import pytest
from flask import g, session
from verba.db import get_db
from sqlalchemy import select, Result
from verba.metadata import metadata

def test_login(client, auth):
    assert client.get('/login').status_code == 200
    result = auth.login()
    assert result.headers["Location"] == "/"
    assert result.status_code == 302

    with client:
        client.get('/')
        assert session.get('user_id') == 1
        assert session['user_id'] == 1
        assert g.user[1] == 'test'

@pytest.mark.parametrize(('email', 'password', 'message'), (('a', 'test', b'Incorrect email address or password'),('test', 'a', b'Incorrect email address or password'),))
def test_login_validation(client, email, password, message):
    result = client.post('/login', data={'email': email, 'password': password})
    assert message in result.data

def test_register(client, app):
    assert client.get('/register').status_code == 200
    
    result = client.post('/register', data={'username': 'register', 'password': 'register', 'confirm_password': 'register', 'firstname': 'verba', 'lastname': 'registrar', 'email': 'null@null.com', 'register': 'Submit'})
    assert b'OTP' in result.data

    with app.app_context():
        users = metadata().tables['users']
        assert Result.fetchone(get_db().execute(select(users))) is not None

@pytest.mark.parametrize(('username', 'password', 'confirm_password', 'firstname', 'lastname', 'email', 'register', 'message'), (
    ('', '', '', '', '', '', 'Submit', b'Username required'),
    ('a', '', '', '', '', '', 'Submit', b'Password required'),
    ('a', 'b', '', '', '', '', 'Submit', b'Passwords do not match'),
    ('a', 'b', 'b', '', '', '', 'Submit', b'This field is required'),
    ('a', 'b', 'b', 'jon', '', '', 'Submit', b'This field is required'),
    ('a', 'b', 'b', 'jon', 'did', '', 'Submit', b'This field is required'),
    ('a', 'b', 'c', 'jon', 'did', '', 'Submit', b'Passwords do not match'),
    ('a', 'b', 'b', 'jon', 'did', 'test@test.com', 'Submit', b'account already exists'),
    ('test', 'b', 'b', 'jon', 'did', 'tester@test.com', 'Submit', b'username has already been taken'),
))
def test_register_validation(client, username, password, confirm_password, firstname, lastname, email, register, message):
    result = client.post(
        '/register',
        data={'username': username, 'password': password, 'confirm_password': confirm_password, 
              'firstname': firstname, 'lastname': lastname, 'email': email, 'register': register}
    )
    assert message in result.data