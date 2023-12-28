import os
import tempfile
import pytest
from verba.app import create_app
from verba.db import get_db, init_db
import sqlalchemy as db


db_password=os.environ.get('DB_PASSWORD')
db_user=os.environ.get('DB_USER')
host=os.environ.get('HOST')
db_name='test'

@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    engine = get_db(engine=db.create_engine(f"mysql://{db_user}:{db_password}@{host}/{db_name}"))