import os
import requests
import pytest

# Base URL for the API, read from environment variable or default to localhost
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# --- Helper functions (mocked for demonstration) ---

def get_auth_token(username, password):
    """Simulates user authentication and returns an auth token."""
    # In a real scenario, this would make a POST request to a login endpoint
    # and parse the token from the response.
    # For this example, we'll return a dummy token based on the username.
    if username == "testuser_a" and password == "passwordA":
        return "dummy_token_for_user_a"
    if username == "testuser_b" and password == "passwordB":
        return "dummy_token_for_user_b"
    return None

# --- Test Cases ---

def test_authenticated_user_views_own_transaction_history():
    """
    Verifies that an authenticated user can view their own transaction history.
    """
    # Authenticate User A
    auth_token = get_auth_token("testuser_a", "passwordA")
    assert auth_token is not None, "Failed to obtain authentication token for User A"

    # Define the endpoint (confirm with API spec)
    # Assuming the endpoint for transaction history is relative to BASE_URL
    transactions_history_endpoint = f"{BASE_URL}/api/v1/transactions/history"

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(transactions_history_endpoint, headers=headers)

    # Assert status code is 200 OK
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"

    # Assert response is a JSON array and contains transactions
    response_json = response.json()
    assert isinstance(response_json, list), "Expected response to be a JSON array"
    assert len(response_json) > 0, "Expected a list of transactions, but got an empty list"

    # Optionally, assert structure of a transaction item
    # if response_json:
    #     first_transaction = response_json[0]
    #     assert "id" in first_transaction
    #     assert "amount" in first_transaction
    #     assert "date" in first_transaction


def test_authenticated_user_cannot_view_another_users_transactions():
    """
    Verifies that an authenticated user cannot view another user's transactions.
    This test assumes there is an endpoint to access a specific transaction by ID
    or a way to request transactions for a specific user ID.
    For demonstration, we'll try to access a specific transaction ID belonging
    to another user.
    """
    # Authenticate User A
    auth_token_a = get_auth_token("testuser_a", "passwordA")
    assert auth_token_a is not None, "Failed to obtain authentication token for User A"

    # Simulate a transaction ID that belongs to User B
    # In a real test, you might create such a transaction via setup or know a pre-existing one.
    transaction_id_of_another_user = "transaction_id_for_user_b_001"

    # Define the endpoint to access a specific transaction (confirm with API spec)
    # If the history endpoint accepted a `userId` parameter for other users, we would test that.
    # Assuming an endpoint like /api/v1/transactions/{transaction_id}
    specific_transaction_endpoint = f"{BASE_URL}/api/v1/transactions/{transaction_id_of_another_user}"

    headers = {
        "Authorization": f"Bearer {auth_token_a}",
        "Content-Type": "application/json"
    }

    # User A attempts to access User B's transaction
    response = requests.get(specific_transaction_endpoint, headers=headers)

    # Assert status code is 403 Forbidden
    assert response.status_code == 403, (
        f"Expected status 403 Forbidden when User A attempts to access User B's transaction, "
        f"got {response.status_code}. Response: {response.text}"
    )
