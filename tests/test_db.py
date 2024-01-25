import pytest
from verba.db import get_db, init_db, close_db
from verba.metadata import metadata
from sqlalchemy import select, exc


def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
    with pytest.raises(exc.ResourceClosedError) as e:
        post = metadata().tables['post']
        db.execute((select(post).where(post.c.id == 1)))
    assert 'closed' in str(e.value)

def test_db_init(monkeypatch, cli_runner, app):
    with app.app_context():
        recorder = {"called": False}

        def record_db_init():
            recorder.update({"called": True})

        monkeypatch.setattr("verba.db.db_init", record_db_init())
        result = cli_runner.invoke(args=['db-init'])
        assert 'initialized' in result.output
        assert recorder['called']


