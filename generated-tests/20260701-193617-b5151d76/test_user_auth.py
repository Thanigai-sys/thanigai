import os
import requests
import pytest

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def test_initiate_payment_with_valid_auth():
    url = f"{BASE_URL}/api/payments/initiate"
    headers = {"Authorization": "Bearer valid_bearer_token"}
    payload = {
        "amount": 100.00,
        "recipient_account": "1234567890",
        "currency": "USD"
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    assert "status" in response.json()

def test_initiate_payment_without_auth():
    url = f"{BASE_URL}/api/payments/initiate"
    payload = {
        "amount": 100.00,
        "recipient_account": "1234567890",
        "currency": "USD"
    }
    response = requests.post(url, json=payload, allow_redirects=False)
    assert response.status_code in [302, 401]
