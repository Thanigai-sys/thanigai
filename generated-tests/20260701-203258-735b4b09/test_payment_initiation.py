import os
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def test_validation_success_complete_valid_data():
    url = f"{BASE_URL}/api/payments/validate"
    payload = {
        "amount": 100.00,
        "currency": "USD",
        "recipient_id": "usr_98213"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") in ["success", "valid", "passed"]

def test_validation_failure_missing_fields_and_negative_amount():
    url = f"{BASE_URL}/api/payments/validate"
    payload = {
        "amount": -50.00
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 400
    errors = response.json()
    assert "recipient_id" in str(errors)
    assert "amount" in str(errors)
