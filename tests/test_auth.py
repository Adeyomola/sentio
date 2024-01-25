import pytest
from flask import g, session

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
    response = client.post('/login', data={'email': email, 'password': password})
    assert message in response.data