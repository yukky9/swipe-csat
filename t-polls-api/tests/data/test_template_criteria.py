import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from data.db_session import SqlAlchemyBase
from data.template_criteria import TemplateCriteria


@pytest.fixture(scope='module')
def session():
    engine = create_engine('sqlite:///:memory:')
    SqlAlchemyBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_template_criteria_model(session):
    template_criteria = TemplateCriteria(
        template_id=1,
        name="Test Template Criteria"
    )

    session.add(template_criteria)
    session.commit()

    assert template_criteria.id is not None
    assert template_criteria.template_id == 1
    assert template_criteria.name == "Test Template Criteria"
