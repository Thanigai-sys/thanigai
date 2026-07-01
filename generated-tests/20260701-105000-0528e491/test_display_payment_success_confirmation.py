import os
import requests
import pytest

# Base URL for the API, read from environment variable or default to localhost
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# Placeholder for the payment endpoint - CONFIRM WITH REAL API SPEC
PAYMENT_ENDPOINT = f"{BASE_URL}/api/v1/payments"

# Placeholder for authentication token/headers
# In a real scenario, this would come from a login API call or test setup
AUTH_HEADERS = {"Authorization": "Bearer test_auth_token"}

def test_payment_success_confirmation_displayed():
    """
    Verifies that a successful payment returns a 200 OK status
    with a confirmation message and transaction details.
    """
    # Step 1: Authenticate a user (represented by AUTH_HEADERS)
    # Step 2: Submit a valid payment request.
    # Step 3: Mock the payment gateway to return a successful transaction.
    #         (Simulated by sending valid payment data that the backend is
    #         configured to process as successful in a test environment).
    payment_data_success = {
        "card_number": "4111222233334444", # A test card number configured for success
        "expiry_date": "12/25",
        "cvv": "123",
        "amount": 100.00,
        "currency": "USD",
        "description": "Test payment for success"
    }

    response = requests.post(PAYMENT_ENDPOINT, json=payment_data_success, headers=AUTH_HEADERS)

    # Step 4: Verify the API response.
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
    response_json = response.json()

    assert "message" in response_json, "Response missing 'message' field for success confirmation"
    assert "Payment successful" in response_json["message"], "Success message not found in response"
    assert "transaction_id" in response_json, "Response missing 'transaction_id' field"
    assert response_json["transaction_id"] is not None, "transaction_id should not be None"

    # Optional: If the API provides a redirect URL to a success page, uncomment and verify
    # assert "redirect_url" in response_json, "Response missing 'redirect_url' field for success page"
    # assert "/success" in response_json["redirect_url"], "Redirect URL does not point to success page"

def test_payment_success_confirmation_not_displayed_on_failure():
    """
    Verifies that a failed payment returns an error status and
    does not include any success confirmation message or redirect to a success page.
    """
    # Step 1: Authenticate a user (represented by AUTH_HEADERS)
    # Step 2: Submit a payment request designed to fail (e.g., declined card).
    # Step 3: Mock the payment gateway to return a failed transaction.
    #         (Simulated by sending payment data that the backend is
    #         configured to process as failed in a test environment, e.g., a 'declined' card number).
    payment_data_failure = {
        "card_number": "4000000000000000", # A test card number configured for failure/decline
        "expiry_date": "12/25",
        "cvv": "123",
        "amount": 50.00,
        "currency": "USD",
        "description": "Test payment for failure"
    }

    response = requests.post(PAYMENT_ENDPOINT, json=payment_data_failure, headers=AUTH_HEADERS)

    # Step 4: Verify the API response.
    # Expecting a client error (e.g., 4xx) or server error (e.g., 5xx) indicating failure
    assert response.status_code >= 400, f"Expected an error status (>=400), got {response.status_code}. Response: {response.text}"

    response_json = response.json()

    # Ensure no success indicators are present
    assert "message" not in response_json or "success" not in response_json.get("message", "").lower(), \
        "Success message found in failure response"
    assert "transaction_id" not in response_json, "Transaction ID found in failure response"
    assert "redirect_url" not in response_json or "/success" not in response_json.get("redirect_url", ""), \
        "Success redirect URL found in failure response"

    assert any(key in response_json for key in ["error", "error_message", "detail", "message"]), \
        "Failure response does not clearly indicate an error with expected fields."
    # Further assertion could be made on the specific error message content if known
    # e.g., assert "declined" in response_json.get("error_message", "").lower()
