import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
import json
from unittest.mock import patch

from gateway.llama_criteria import generate_criteria


@patch('gateway.llama_criteria.requests.get')
def test_generate_criteria(mock_get):
    mock_response = {
        "criteria": "This is a test criteria"
    }
    mock_get.return_value.content = json.dumps(mock_response)

    name = "Test Name"
    response = generate_criteria(name)

    assert response == mock_response
    mock_get.assert_called_once_with(
        "http://kowlad123321456654.tplinkdns.com/api/llama/criteria",
        params={"name": name},
        timeout=300
    )
