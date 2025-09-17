import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from data.db_session import SqlAlchemyBase
from data.special import Special


@pytest.fixture(scope='module')
def session():
    engine = create_engine('sqlite:///:memory:')
    SqlAlchemyBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_special_model(session):
    special = Special(
        poll_id=1,
        question="Test Question",
        answer=True
    )

    session.add(special)
    session.commit()

    assert special.id is not None
    assert special.poll_id == 1
    assert special.question == "Test Question"
    assert special.answer is True
