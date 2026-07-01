import os
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def test_successful_api_request_authentication():
    url = f"{BASE_URL}/api/payments/initiate"
    headers = {"Authorization": "Bearer mock_valid_token_123"}
    response = requests.post(url, headers=headers, json={})
    assert response.status_code == 200
    data = response.json()
    assert "session_token" in data or "initiation_session_token" in data

def test_api_redirection_and_auth_error_missing_header():
    url = f"{BASE_URL}/api/payments/initiate"
    response = requests.post(url, json={}, allow_redirects=False)
    assert response.status_code in [401, 302]
    if response.status_code == 302:
        assert "Location" in response.headers or "login" in response.url
    else:
        data = response.json()
        assert "error" in data or "detail" in data
