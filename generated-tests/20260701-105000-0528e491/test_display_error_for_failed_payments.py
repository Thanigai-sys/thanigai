import os
import requests
import pytest

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# Placeholder for a valid authentication token. In a real scenario, this would come
# from a login fixture or a pre-test setup.
# For simplicity, we'll use a dummy token.
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsImlhdCI6MTUxNjIzOTAyMn0.SflKxwRJSMeKKF2QT4fwp_pysKZfoVwa_z-66-8H2-Q"

# Placeholder for the payment endpoint. This should be confirmed against the real API spec.
PAYMENT_ENDPOINT = f"{BASE_URL}/api/v1/payments"

def test_display_clear_error_for_failed_payment():
    """
    Verifies that the API returns a 4xx status and a clear, user-friendly
    error message for a payment failure due to insufficient funds.
    Assumes the backend is configured to simulate 'insufficient_funds'
    based on a specific card number or payment data.
    """
    headers = {
        "Authorization": AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    # This card number is a hypothetical value that the backend
    # would recognize as triggering an 'insufficient_funds' error.
    payment_data = {
        "card_number": "4111222233334444", # Hypothetical card for insufficient funds
        "expiration_month": "12",
        "expiration_year": "2025",
        "cvv": "123",
        "amount": 100.00,
        "currency": "USD"
    }

    response = requests.post(PAYMENT_ENDPOINT, json=payment_data, headers=headers)

    # The requirement states 400 Bad Request or 402 Payment Required
    assert response.status_code in [400, 402], \
        f"Expected status 400 or 402, but got {response.status_code}"

    response_json = response.json()
    assert "error" in response_json, "Expected 'error' field in response"
    assert "Payment failed: Insufficient Funds" in response_json["error"], \
        f"Expected clear 'Insufficient Funds' error message, got '{response_json['error']}'"

def test_display_ambiguous_error_for_payment_failure():
    """
    Verifies that the API returns an error status but with a generic or
    ambiguous message when a specific failure reason is not meant to be
    exposed or is handled poorly by the backend.
    Assumes the backend is configured to simulate a failure that leads to
    a generic error message (e.g., for an expired card not explicitly
    handled to give a specific user-friendly message).
    """
    headers = {
        "Authorization": AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    # This card number is a hypothetical value that the backend
    # would recognize as an expired card leading to a generic error.
    payment_data = {
        "card_number": "5111222233334444", # Hypothetical card for generic failure (e.g., expired)
        "expiration_month": "01",
        "expiration_year": "2020", # Deliberately expired
        "cvv": "456",
        "amount": 50.00,
        "currency": "USD"
    }

    response = requests.post(PAYMENT_ENDPOINT, json=payment_data, headers=headers)

    # The requirement implies an error status (4xx)
    assert response.status_code >= 400 and response.status_code < 500, \
        f"Expected a 4xx status code, but got {response.status_code}"

    response_json = response.json()
    assert "error" in response_json, "Expected 'error' field in response"
    
    # Check for a generic error message, and ensure it's not too specific
    generic_message_part = "An error occurred"
    assert generic_message_part in response_json["error"], \
        f"Expected generic error message part '{generic_message_part}', got '{response_json['error']}'"
    
    # Negative check: ensure it doesn't contain specific failure details
    # This is key for the "ambiguous" part of the negative test.
    specific_failure_details = ["Insufficient Funds", "Expired Card", "Invalid CVV"]
    for detail in specific_failure_details:
        assert detail not in response_json["error"], \
            f"Error message should be ambiguous, but contained '{detail}': {response_json['error']}"
