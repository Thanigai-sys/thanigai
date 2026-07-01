import os
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def test_retrieve_transaction_history_valid_filter():
    url = f"{BASE_URL}/api/transactions"
    params = {
        "start_date": "2023-10-01",
        "end_date": "2023-10-31"
    }
    response = requests.get(url, params=params)
    assert response.status_code == 200
    transactions = response.json()
    assert isinstance(transactions, list)
    for txn in transactions:
        timestamp = txn.get("timestamp", "")
        assert timestamp >= "2023-10-01" and timestamp <= "2023-10-31T23:59:59"

def test_retrieve_transaction_history_invalid_filter():
    url = f"{BASE_URL}/api/transactions"
    params = {
        "start_date": "2023-10-31",
        "end_date": "2023-10-01"
    }
    response = requests.get(url, params=params)
    assert response.status_code == 400
    error_msg = response.json()
    assert "start_date" in str(error_msg) or "chronologically" in str(error_msg) or "invalid" in str(error_msg).lower()
