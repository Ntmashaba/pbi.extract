import pytest
import requests_mock
from services.api_service import ApiService

@pytest.fixture
def api_service():
    connection_args = {
        'power_bi_api_url': 'https://example.com/api/v1',
        'headers': {
            'Content-Type': 'application/json'
        }
    }
    return ApiService(**connection_args)

def test_get_endpoint_success(api_service):
    # Mock the requests.get method to return a success response
    with requests_mock.Mocker() as m:
        endpoint_url = 'https://example.com/api/v1/data'
        response_data = {'value': [{'id': 1, 'name': 'data1'}, {'id': 2, 'name': 'data2'}]}
        m.get(endpoint_url, json=response_data, status_code=200)

        # Call get_endpoint with a valid endpoint URL
        result = api_service.get_endpoint('/data')

        # Verify the result is as expected
        assert result == response_data['value']

def test_get_endpoint_failure(api_service):
    # Mock the requests.get method to return a failure response
    with requests_mock.Mocker() as m:
        endpoint_url = 'https://example.com/api/v1/data'
        error_message = 'Failed to get endpoint: /data'
        m.get(endpoint_url, text=error_message, status_code=500)

        # Call get_endpoint with an invalid endpoint URL
        with pytest.raises(Exception) as excinfo:
            api_service.get_endpoint('/data')
        
        # Verify that an exception was raised with the expected error message
        assert str(excinfo.value) == error_message
