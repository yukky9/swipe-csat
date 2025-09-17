import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from data.db_session import SqlAlchemyBase
from data.user_polls import UserPoll


@pytest.fixture(scope='module')
def session():
    engine = create_engine('sqlite:///:memory:')
    SqlAlchemyBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_user_poll_model(session):
    user_poll = UserPoll(
        user_id="test_user",
        poll_id=1,
        criterion_name_1="Criterion 1",
        criterion_rating_1=5,
        criterion_name_2="Criterion 2",
        criterion_rating_2=4,
        criterion_name_3="Criterion 3",
        criterion_rating_3=3,
        checking_question="Test Question",
        checking_result=True
    )

    session.add(user_poll)
    session.commit()

    assert user_poll.id is not None
    assert user_poll.user_id == "test_user"
    assert user_poll.poll_id == 1
    assert user_poll.criterion_name_1 == "Criterion 1"
    assert user_poll.criterion_rating_1 == 5
    assert user_poll.criterion_name_2 == "Criterion 2"
    assert user_poll.criterion_rating_2 == 4
    assert user_poll.criterion_name_3 == "Criterion 3"
    assert user_poll.criterion_rating_3 == 3
    assert user_poll.checking_question == "Test Question"
    assert user_poll.checking_result is True
