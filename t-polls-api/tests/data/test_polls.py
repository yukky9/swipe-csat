import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from data.db_session import SqlAlchemyBase
from data.polls import Poll


@pytest.fixture(scope='module')
def session():
    engine = create_engine('sqlite:///:memory:')
    SqlAlchemyBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_poll_model(session):
    poll = Poll(
        name="Test Poll",
        description="This is a test poll",
        date=datetime.utcnow(),
        respondent_amount=10,
        rating=5
    )

    session.add(poll)
    session.commit()

    assert poll.id is not None
    assert poll.name == "Test Poll"
    assert poll.description == "This is a test poll"
    assert poll.respondent_amount == 10
    assert poll.rating == 5


def test_poll_relationships(session):
    poll = Poll(
        name="Test Poll with Relationships",
        description="This is a test poll with relationships"
    )

    session.add(poll)
    session.commit()

    assert len(poll.criteria) == 0
    assert len(poll.special) == 0
