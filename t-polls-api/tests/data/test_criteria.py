import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from data.db_session import SqlAlchemyBase
from data.criteria import Criterion


@pytest.fixture(scope='module')
def session():
    engine = create_engine('sqlite:///:memory:')
    SqlAlchemyBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_criterion_model(session):
    criterion = Criterion(
        poll_id=1,
        name="Test Criterion",
        one_point_amount=5,
        two_points_amount=4,
        three_points_amount=3,
        four_points_amount=2,
        five_points_amount=1,
        csat=90
    )

    session.add(criterion)
    session.commit()

    assert criterion.id is not None
    assert criterion.poll_id == 1
    assert criterion.name == "Test Criterion"
    assert criterion.one_point_amount == 5
    assert criterion.two_points_amount == 4
    assert criterion.three_points_amount == 3
    assert criterion.four_points_amount == 2
    assert criterion.five_points_amount == 1
    assert criterion.csat == 90
