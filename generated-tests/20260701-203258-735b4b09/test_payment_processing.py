import os
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def test_successful_payment_processing_and_txn_id():
    url = f"{BASE_URL}/api/payments/process"
    payload = {
        "gateway_token": "tok_sandbox_success"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "transaction_id" in data
    assert data.get("status") == "SUCCESS"

def test_processing_failure_declined_token():
    url = f"{BASE_URL}/api/payments/process"
    payload = {
        "gateway_token": "tok_sandbox_decline"
    }
    response = requests.post(url, json=payload)
    assert response.status_code in [400, 422]
    data = response.json()
    assert "error" in data or "message" in data or "decline" in str(data).lower()
