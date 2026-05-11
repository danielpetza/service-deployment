import sys
import os
import pytest
from app import create_app
from extensions import db
from models import ThoughtModel

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

@pytest.fixture
def client():
    config = {"SQLALCHEMY_DATABASE_URI":os.environ.get("DATABASE_URL"), "SQLALCHEMY_TRACK_MODIFICATIONS":False}
    app = create_app(config)
    with app.test_client():
        db.create_all()
        yield 
        db.session.remove()
        db.drop_all()

def test_db_integration_postgres(app_context):
    thought = ThoughtModel(username="postgres_user", text="Dato reale")
    db.session.add(thought)
    db.session.commit()

    result = ThoughtModel.query.filter_by(username="postgres_user").first()
    assert result is not None
    assert result.text == "Dato reale"

    db.session.delete(result)
    db.session.commit()

    result2 = ThoughtModel.query.filter_by(username="postgres_user").first()
    assert result2 is None