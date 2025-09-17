import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from data.db_session import SqlAlchemyBase
from data.users import User


@pytest.fixture(scope='module')
def session():
    engine = create_engine('sqlite:///:memory:')
    SqlAlchemyBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_user_model(session):
    user = User(
        id="test_user",
        username="Test User",
        polls_amount=5,
        light_theme=True,
        swipe_mode=False,
        last_request=datetime.utcnow()
    )

    session.add(user)
    session.commit()

    assert user.id == "test_user"
    assert user.username == "Test User"
    assert user.polls_amount == 5
    assert user.light_theme is True
    assert user.swipe_mode is False
    assert isinstance(user.last_request, datetime)
    assert len(user.polls) == 0
