import pytest
from verba.db import get_db
import tempfile
import os

def test_index(client):
    result = client.get('/')
    assert b'Our Top Picks' in result.data
    assert b'test title' in result.data

def test_home(client, auth):
    auth.login()
    result = client.get('/')
    assert b'Hi! test' in result.data
    assert b'test title' in result.data

def test_write(client, auth):
    assert client.get('/write').headers["Location"] == "/login"
    assert client.get('/write').status_code == 302

    auth.login()
    result = client.get('/write')
    assert b'placeholder="Title:"' in result.data
    assert result.status_code == 200

    post_result = client.post('/write', data={'title': 'Testing Write', 'body': 'This is a test', 'image_url': 'https://verba.fly.dev'})
    assert post_result.headers["Location"] == "/"
    assert b'Hi! test' in client.get('/').data
    assert b'Testing Write' in client.get('/').data

    auth.logout()
    test_index(client)