import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from data.db_session import SqlAlchemyBase
from data.templates import Template


@pytest.fixture(scope='module')
def session():
    engine = create_engine('sqlite:///:memory:')
    SqlAlchemyBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_template_model(session):
    template = Template(
        name="Test Template"
    )

    session.add(template)
    session.commit()

    assert template.id is not None
    assert template.name == "Test Template"
    assert len(template.template_criteria) == 0
