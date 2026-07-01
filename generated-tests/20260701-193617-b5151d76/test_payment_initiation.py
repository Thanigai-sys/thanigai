import os
import requests
import pytest

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def test_payment_initiation_with_valid_fields():
    url = f"{BASE_URL}/api/payments/validate"
    headers = {"Authorization": "Bearer valid_bearer_token"}
    payload = {
        "amount": 250.00,
        "recipient_account": "9876543210",
        "currency": "USD"
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") in ["Success", "Valid"]

def test_payment_initiation_missing_mandatory_fields():
    url = f"{BASE_URL}/api/payments/validate"
    headers = {"Authorization": "Bearer valid_bearer_token"}
    payload = {
        "recipient_account": "invalid_acc_format",
        "currency": "USD"
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "errors" in data or "error" in data
