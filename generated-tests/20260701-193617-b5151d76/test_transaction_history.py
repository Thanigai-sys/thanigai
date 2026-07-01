import os
import requests
import pytest

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def test_retrieve_transactions_filtered_by_date():
    url = f"{BASE_URL}/api/transactions"
    headers = {"Authorization": "Bearer valid_bearer_token"}
    params = {
        "start_date": "2023-01-01",
        "end_date": "2023-01-31"
    }
    response = requests.get(url, params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for tx in data:
        assert "date" in tx
        assert "2023-01-01" <= tx["date"] <= "2023-01-31"

def test_retrieve_transactions_invalid_date_format():
    url = f"{BASE_URL}/api/transactions"
    headers = {"Authorization": "Bearer valid_bearer_token"}
    params = {
        "start_date": "not-a-date"
    }
    response = requests.get(url, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
