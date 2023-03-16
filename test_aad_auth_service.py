from unittest.mock import patch
from msal.exceptions import MsalServiceError
from services.aad_auth_service import AadAuthService
import pytest


@patch("services.aad_auth_service.ConfidentialClientApplication")
def test_get_access_token_success(mock_app):
    # Set up the mock response for a successful token acquisition
    mock_token = {"access_token": "test_access_token"}
    mock_app.return_value.acquire_token_for_client.return_value = mock_token

    # Initialize an instance of AadAuthService
    auth_service = AadAuthService(
        auth_url="https://login.microsoftonline.com/common",
        tenant_id="test_tenant_id",
        client_id="test_client_id",
        client_secret="test_client_secret",
        scope_base="test_scope_base"
    )

    # Call the method under test
    access_token = auth_service.get_access_token()

    # Verify the result
    assert access_token == mock_token["access_token"]
    mock_app.assert_called_once_with(
        "test_client_id",
        authority="https://login.microsoftonline.com/test_tenant_id",
        client_credential="test_client_secret",
    )
    mock_app.return_value.acquire_token_for_client.assert_called_once_with(scopes=["test_scope_base"])


# @patch("services.aad_auth_service.ConfidentialClientApplication")
# def test_get_access_token_failure(mock_app):
#     # Set up the mock response for a failed token acquisition
#     mock_error = MsalServiceError(
#         "test_error",
#         {"error_description": "test_error_description"},
#         error_description="test_error_description",
#     )
#     mock_app.return_value.acquire_token_for_client.side_effect = mock_error

#     # Initialize an instance of AadAuthService
#     auth_service = AadAuthService(
#         auth_url="https://login.microsoftonline.com/common",
#         tenant_id="test_tenant_id",
#         client_id="test_client_id",
#         client_secret="test_client_secret",
#         scope_base="test_scope_base"
#     )

#     # Call the method under test and catch the exception
#     try:
#         access_token = auth_service.get_access_token()
#     except Exception as e:
#         assert str(e) == "Failed to acquire access token: test_error_description"
#     else:
#         assert False, "Expected exception not raised"

#     mock_app.assert_called_once_with(
#         "test_client_id",
#         authority="https://login.microsoftonline.com/test_tenant_id",
#         client_credential="test_client_secret",
#     )
#     mock_app.return_value.acquire_token_for_client.assert_called_once_with(scopes=["test_scope_base"])

# @patch("services.aad_auth_service.ConfidentialClientApplication")
# def test_get_access_token_failure_no_access_token(mock_app):
#     # Set up the mock response for a failed token acquisition with no access token
#     mock_error = {"error_description": "test_error_description"}
#     mock_app.return_value.acquire_token_for_client.return_value = mock_error

#     # Initialize an instance of AadAuthService
#     auth_service = AadAuthService(
#         auth_url="https://login.microsoftonline.com/common",
#         tenant_id="test_tenant_id",
#         client_id="test_client_id",
#         client_secret="test_client_secret",
#         scope_base="test_scope_base"
#     )

#     # Call the method under test and catch the exception
#     with pytest.raises(ValueError) as e:
#         access_token = auth_service.get_access_token()

#     assert str(e.value) == "Access token not found in response"

#     mock_app.assert_called_once_with(
#         "test_client_id",
#         client_credential="test_client_secret",
#         authority="https://login.microsoftonline.com/test_tenant_id",
#     )
#     mock_app.return_value.acquire_token_for_client.assert_called_once_with(scopes=["test_scope_base"])
