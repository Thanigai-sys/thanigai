import os
import requests
import pytest

# Base URL for the API, read from an environment variable or default to localhost
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# Placeholder for API endpoint - confirm with actual API specification
PAYMENTS_ENDPOINT = f"{BASE_URL}/api/v1/payments"

# A placeholder for authentication headers. In a real scenario, this would come
# from a login fixture or a pre-defined token.
AUTH_HEADERS = {
    "Authorization": "Bearer mock_auth_token_123",
    "Content-Type": "application/json"
}

def get_valid_payment_payload():
    """Returns a dictionary representing a valid payment request payload."""
    return {
        "cardNumber": "4111222233334444",
        "expiryDate": "12/25",
        "cvv": "123",
        "amount": 100.50,
        "currency": "USD",
        "cardHolderName": "John Doe" # Added as a common mandatory field, though not explicitly listed in problem
    }


def test_submit_payment_with_all_mandatory_fields_valid():
    """
    Verifies that submitting a payment request with all mandatory fields populated
    with valid data results in a 200 OK status.
    """
    payload = get_valid_payment_payload()

    response = requests.post(PAYMENTS_ENDPOINT, json=payload, headers=AUTH_HEADERS)

    assert response.status_code == 200, (
        f"Expected status code 200 for valid payment, but got {response.status_code}. "
        f"Response: {response.text}"
    )
    # Further assertions could include checking for a 'transactionId' or 'status' field
    # in the response body, depending on API design.
    response_json = response.json()
    assert "message" in response_json or "status" in response_json, \
        f"Response for valid payment missing expected success indicator. Response: {response.text}"
    # Example: if the API returns a processing status or transaction ID
    # assert response_json.get("status") == "processing" or response_json.get("transactionId") is not None


def test_submit_payment_with_missing_mandatory_field():
    """
    Verifies that submitting a payment request with a missing mandatory field
    (e.g., 'cardNumber') results in a 400 Bad Request status and an appropriate
    error message.
    """
    payload = get_valid_payment_payload()
    del payload["cardNumber"] # Intentionally omit 'cardNumber'

    response = requests.post(PAYMENTS_ENDPOINT, json=payload, headers=AUTH_HEADERS)

    assert response.status_code == 400, (
        f"Expected status code 400 for missing mandatory field, but got {response.status_code}. "
        f"Response: {response.text}"
    )

    response_json = response.json()
    assert "error" in response_json or "message" in response_json, \
        f"Response for missing field did not contain an error message. Response: {response.text}"

    # Check for a specific error message indicating the missing field
    error_message = response_json.get("error", response_json.get("message", "")).lower()
    assert "cardnumber is required" in error_message or \
           "missing cardnumber" in error_message or \
           "invalid payload" in error_message,
        f"Error message did not clearly indicate missing 'cardNumber'. Response: {response.text}"
