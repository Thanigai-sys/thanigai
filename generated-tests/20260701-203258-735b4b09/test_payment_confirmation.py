import os
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def test_payment_confirmation_success():
    url = f"{BASE_URL}/api/payments/confirm"
    payload = {
        "transaction_id": "TXN_VALID_123"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "CONFIRMED"
    assert data.get("email_sent") is True

def test_payment_confirmation_non_existent():
    url = f"{BASE_URL}/api/payments/confirm"
    payload = {
        "transaction_id": "TXN_NULL"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 404
    data = response.json()
    assert "not found" in str(data).lower() or "exist" in str(data).lower()
