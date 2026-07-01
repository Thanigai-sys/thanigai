import os
import requests
import pytest

# Base URL for the API, read from environment variable or default to localhost
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# Placeholder for the payments endpoint. Confirm with actual API spec.
PAYMENTS_ENDPOINT = f"{BASE_URL}/api/v1/payments"

# --- Fixtures or setup for authentication ---
# In a real scenario, this would involve logging in or getting a token.
# For this example, we'll use a dummy token.
@pytest.fixture(scope="module")
def auth_headers():
    """Provides authentication headers for API requests."""
    # Simulate obtaining an authentication token
    # In a real application, this would involve a login request
    # and extracting the token from the response.
    dummy_token = "your_secure_auth_token_here"
    headers = {
        "Authorization": f"Bearer {dummy_token}",
        "Content-Type": "application/json"
    }
    return headers


# --- Test Cases ---

def test_submit_payment_with_valid_amount(auth_headers):
    """
    Verifies that a payment request with a valid positive numeric amount is accepted.
    (REQ-005: Validate Payment Amount - Positive Case)
    """
    # Test Case: Submit Payment with Valid Amount
    # Steps:
    # 1. Authenticate a user (handled by auth_headers fixture).
    # 2. Construct a payment request with a positive numeric amount, e.g., 100.00.
    # 3. Send POST request to /payments with the valid amount.
    
    valid_amount = 100.00
    payload = {"amount": valid_amount, "currency": "USD", "description": "Test Payment"}

    response = requests.post(PAYMENTS_ENDPOINT, json=payload, headers=auth_headers)

    # Expected Result: The API accepts the request, returning a 200 OK status,
    # indicating the payment amount passed validation.
    assert response.status_code == 200, \
        f"Expected status 200 for valid amount {valid_amount}, got {response.status_code}. Response: {response.text}"
    
    # Optionally, further assertions can be made on the response body
    # to confirm the payment creation or validation success.
    response_json = response.json()
    assert "id" in response_json or "message" in response_json, \
        f"Response body missing expected success indicator: {response.text}"


@pytest.mark.parametrize("invalid_amount, expected_error_part", [
    (0, "positive"),                    # Zero amount
    (-50.00, "positive"),               # Negative amount
    ("abc", "format"),                 # Non-numeric amount
    (1000000000000.00, "limit")         # Amount exceeding a theoretical max limit
])
def test_submit_payment_with_invalid_amount(auth_headers, invalid_amount, expected_error_part):
    """
    Verifies that payment requests with various invalid amounts are rejected with a 400 Bad Request status.
    (REQ-005: Validate Payment Amount - Negative Cases)
    """
    # Test Case: Submit Payment with Invalid Amount
    # Steps:
    # 1. Authenticate a user (handled by auth_headers fixture).
    # 2. Attempt to submit payments with various invalid amounts.
    # 3. Send POST requests to /payments for each invalid amount.

    payload = {"amount": invalid_amount, "currency": "USD", "description": "Invalid Test Payment"}

    response = requests.post(PAYMENTS_ENDPOINT, json=payload, headers=auth_headers)

    # Expected Result: The API rejects each request with an invalid amount,
    # returning a 400 Bad Request status and an appropriate error message.
    assert response.status_code == 400, \
        f"Expected status 400 for invalid amount '{invalid_amount}', got {response.status_code}. Response: {response.text}"
    
    response_json = response.json()
    assert "message" in response_json or "errors" in response_json, \
        f"Response body missing expected error message for '{invalid_amount}': {response.text}"
    
    # Assert that the error message contains a relevant keyword indicating the reason for failure.
    error_message_lower = str(response_json.get("message", response_json.get("errors", ""))).lower()
    assert expected_error_part in error_message_lower or "invalid" in error_message_lower or "bad request" in error_message_lower, \
        f"Error message for '{invalid_amount}' did not contain expected part '{expected_error_part}'. Message: {error_message_lower}"
