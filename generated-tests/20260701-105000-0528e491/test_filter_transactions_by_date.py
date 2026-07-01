import os
import requests
import pytest
from datetime import datetime

# Base URL for the API, read from environment variable or default
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# Placeholder for the transactions endpoint. Confirm with actual API spec.
TRANSACTIONS_ENDPOINT = f"{BASE_URL}/api/v1/transactions/history"

@pytest.fixture(scope="module")
def auth_headers():
    """Simulates user authentication and returns headers with an auth token."""
    # In a real scenario, this would involve a login request to obtain a token.
    # For this test, we'll use a dummy token.
    dummy_token = "your_auth_token_here"
    headers = {
        "Authorization": f"Bearer {dummy_token}",
        "Content-Type": "application/json"
    }
    # You might want to add a check here to ensure the token is valid or obtained successfully
    # e.g., by making a simple authenticated request.
    print(f"\nUsing auth headers: {headers}") # For debugging
    return headers


def test_filter_transaction_history_by_valid_date_range(auth_headers):
    """
    Verifies that filtering transaction history by a valid date range returns
    only transactions within that range with a 200 OK status.
    """
    print(f"\nTesting valid date range filtering on {TRANSACTIONS_ENDPOINT}")
    start_date = "2023-01-01"
    end_date = "2023-01-31"
    params = {
        "startDate": start_date,
        "endDate": end_date
    }

    response = requests.get(TRANSACTIONS_ENDPOINT, headers=auth_headers, params=params)

    assert response.status_code == 200, \
        f"Expected status 200 for valid date range, got {response.status_code}. Response: {response.text}"
    
    transactions = response.json()
    assert isinstance(transactions, list), "Expected response to be a list of transactions"

    # Assuming each transaction has a 'date' field in ISO format (e.g., '2023-01-15T10:30:00Z')
    # Adjust 'date' field name based on actual API response structure.
    for transaction in transactions:
        assert "transaction_date" in transaction, "Transaction missing 'transaction_date' field"
        transaction_datetime = datetime.fromisoformat(transaction["transaction_date"].replace('Z', '+00:00'))
        
        # Check if the transaction date falls within the specified range
        assert datetime.fromisoformat(start_date) <= transaction_datetime.replace(tzinfo=None) <= datetime.fromisoformat(end_date).replace(hour=23, minute=59, second=59, microsecond=999999).replace(tzinfo=None), \
            f"Transaction date {transaction['transaction_date']} is outside the range {start_date} - {end_date}"


def test_filter_transaction_history_by_invalid_date_range(auth_headers):
    """
    Verifies that filtering transaction history with an invalid or malformed
    date range returns a 400 Bad Request status.
    """
    print(f"\nTesting invalid date range filtering on {TRANSACTIONS_ENDPOINT}")

    # Test case 1: endDate is before startDate
    invalid_params_order = {
        "startDate": "2023-02-01",
        "endDate": "2023-01-01"
    }
    response_order = requests.get(TRANSACTIONS_ENDPOINT, headers=auth_headers, params=invalid_params_order)
    assert response_order.status_code == 400, \
        f"Expected status 400 for endDate before startDate, got {response_order.status_code}. Response: {response_order.text}"
    assert "invalid date range" in response_order.text.lower() or \
           "start date cannot be after end date" in response_order.text.lower(), \
        f"Expected error message for invalid date order, got: {response_order.text}"

    # Test case 2: Malformed startDate
    malformed_params_start = {
        "startDate": "invalid-date",
        "endDate": "2023-01-31"
    }
    response_malformed_start = requests.get(TRANSACTIONS_ENDPOINT, headers=auth_headers, params=malformed_params_start)
    assert response_malformed_start.status_code == 400, \
        f"Expected status 400 for malformed startDate, got {response_malformed_start.status_code}. Response: {response_malformed_start.text}"
    assert "malformed date" in response_malformed_start.text.lower() or \
           "invalid date format" in response_malformed_start.text.lower(), \
        f"Expected error message for malformed startDate, got: {response_malformed_start.text}"

    # Test case 3: Malformed endDate
    malformed_params_end = {
        "startDate": "2023-01-01",
        "endDate": "not-a-date"
    }
    response_malformed_end = requests.get(TRANSACTIONS_ENDPOINT, headers=auth_headers, params=malformed_params_end)
    assert response_malformed_end.status_code == 400, \
        f"Expected status 400 for malformed endDate, got {response_malformed_end.status_code}. Response: {response_malformed_end.text}"
    assert "malformed date" in response_malformed_end.text.lower() or \
           "invalid date format" in response_malformed_end.text.lower(), \
        f"Expected error message for malformed endDate, got: {response_malformed_end.text}"