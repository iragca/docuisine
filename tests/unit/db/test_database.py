from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from docuisine.db.models import Base, User

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # keeps the DB alive
)

Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


def test_insert_user(db_session):
    test_username = "testuser"
    new_user = User(username=test_username, password="hashedpassword")

    db_session.add(new_user)
    db_session.commit()

    results = db_session.query(User).filter(User.username == test_username).all()
    assert len(results) == 1
    assert results[0].username == test_username
    assert isinstance(results[0].created_at, datetime), (
        f"created_at should be a datetime, got {type(results[0].created_at)}"
    )
