import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
import json
from unittest.mock import patch

from gateway.llama_analysis import generate_analysis


@patch('gateway.llama_analysis.requests.get')
def test_generate_analysis(mock_get):
    mock_response = {
        "analysis": "This is a test analysis"
    }
    mock_get.return_value.content = json.dumps(mock_response)

    name = "Test Name"
    criteria = "Test Criteria"
    response = generate_analysis(name, criteria)

    assert response == mock_response
    mock_get.assert_called_once_with(
        "http://kowlad123321456654.tplinkdns.com/api/llama/analysis",
        params={"name": name, "criteria": criteria},
        timeout=300
    )
