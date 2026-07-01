import os
import requests
import pytest

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def test_confirm_payment_and_email_dispatch():
    url = f"{BASE_URL}/api/payments/confirm"
    headers = {"Authorization": "Bearer valid_bearer_token"}
    payload = {
        "transaction_id": "TXN-100200300"
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data.get("email_dispatched") is True

def test_confirm_payment_invalid_id():
    url = f"{BASE_URL}/api/payments/confirm"
    headers = {"Authorization": "Bearer valid_bearer_token"}
    payload = {
        "transaction_id": "INVALID-ID-999"
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
