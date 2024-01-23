import os
import tempfile
import pytest
from verba.app import create_app
from verba.db import get_db, init_db
from sqlalchemy import insert

dbms="sqlite3"

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    db_name=db_path

    app = create_app()

    md = get_db(dbms)[1]
    users = md.tables["users"]
    post = md.tables["post"]

    create_user = (insert(users),
            [
        {"username": "test", "password": "pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f", "firstname": "tester", "lastname": "testing", "email": "test@test.com"},
        {"username": "other", "password": "pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79", "firstname": "other", "lastname": "tester", "email": "jon@doe.com"}
            ]
        )
    insert_post = (insert(post).values(title="test title", author_id="1", firstname="tester", body="test body"))

    with app.app_context():
        init_db(dbms)
        get_db(dbms)[0].connect().execute(insert_post)
    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()