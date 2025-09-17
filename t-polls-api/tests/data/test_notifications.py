import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from data.db_session import SqlAlchemyBase
from data.notifications import Notification


@pytest.fixture(scope='module')
def session():
    engine = create_engine('sqlite:///:memory:')
    SqlAlchemyBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_notification_model(session):
    notification = Notification(
        name="Test Notification",
        time=datetime.utcnow()
    )

    session.add(notification)
    session.commit()

    assert notification.id is not None
    assert notification.name == "Test Notification"
    assert isinstance(notification.time, datetime)
