import os
import requests
import pytest

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def test_process_payment_gateway_success():
    url = f"{BASE_URL}/api/payments/process"
    headers = {"Authorization": "Bearer valid_bearer_token"}
    payload = {
        "amount": 500.00,
        "recipient_account": "1234567890",
        "currency": "USD",
        "gateway_simulation": "success"
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code in [200, 201]
    data = response.json()
    assert "transaction_id" in data
    assert data.get("status") == "success"

def test_process_payment_gateway_failure():
    url = f"{BASE_URL}/api/payments/process"
    headers = {"Authorization": "Bearer valid_bearer_token"}
    payload = {
        "amount": 9999999.00,
        "recipient_account": "1234567890",
        "currency": "USD",
        "gateway_simulation": "insufficient_funds"
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code in [422, 502]
    data = response.json()
    assert "error" in data
