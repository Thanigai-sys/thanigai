import os
import requests
import pytest

# Base URL for the API, read from environment variable or default to localhost
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# Placeholder for the payment processing endpoint.
# This should be confirmed against the actual API specification.
PAYMENT_ENDPOINT = f"{BASE_URL}/api/v1/payments" # Assuming a /payments endpoint for processing

# --- Helper functions (mocked for the purpose of this script) ---
# In a real scenario, this would involve a login request to get a real token.
def get_auth_token():
    """
    Simulates getting an authentication token.
    In a real test, this would involve making a login request to the API
    and returning a valid token (e.g., JWT).
    """
    # For demonstration, returning a dummy token.
    # Replace with actual authentication logic if required by the API.
    return "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIxMjMifQ.dummy_token"

# --- Test Functions ---

def test_transaction_id_generated_upon_successful_payment():
    """
    Verifies that a unique transaction ID is generated and returned upon a successful payment.
    This test assumes the API under test has a mechanism (e.g., a specific payment_method_token)
    to simulate a successful payment gateway response in a test environment.
    """
    headers = {
        "Authorization": get_auth_token(),
        "Content-Type": "application/json"
    }

    # Data to simulate a successful payment gateway response.
    # In a real scenario, `payment_method_token` might be a token representing a valid card
    # that the backend is configured to process successfully in a test mode.
    payment_data = {
        "amount": 100.00,
        "currency": "USD",
        "payment_method_token": "test_token_success", # This token signifies success to the backend
        "description": "Test payment for successful ID generation"
    }

    response = requests.post(PAYMENT_ENDPOINT, headers=headers, json=payment_data)

    assert response.status_code == 200, \
        f"Expected status 200 OK for successful payment, got {response.status_code}. Response: {response.text}"
    
    response_json = response.json()

    assert "transactionId" in response_json, "Response body must contain 'transactionId' for successful payments"
    assert isinstance(response_json["transactionId"], str), "transactionId must be a string"
    assert len(response_json["transactionId"]) > 0, "transactionId must not be empty"

    # In a more comprehensive test, you might also query a dedicated status/lookup endpoint
    # to verify the transaction ID is indeed stored in the system.


def test_no_transaction_id_generated_for_failed_payment():
    """
    Verifies that no transaction ID is generated and returned for a failed payment.
    This test assumes the API under test has a mechanism (e.g., a specific payment_method_token)
    to simulate a failed payment gateway response in a test environment.
    """
    headers = {
        "Authorization": get_auth_token(),
        "Content-Type": "application/json"
    }

    # Data to simulate a failed payment gateway response.
    # `payment_method_token` here would represent a card/token that the backend is
    # configured to recognize as failing a payment in test mode.
    payment_data = {
        "amount": 50.00,
        "currency": "EUR",
        "payment_method_token": "test_token_failure", # This token signifies failure to the backend
        "description": "Test payment for failed ID generation"
    }

    response = requests.post(PAYMENT_ENDPOINT, headers=headers, json=payment_data)

    # Expected error status code. This can vary (e.g., 400 Bad Request, 422 Unprocessable Entity,
    # 500 Internal Server Error) depending on how the API handles payment gateway failures.
    # We assert it's not a success (2xx) status code.
    assert not (200 <= response.status_code < 300), \
        f"Expected an error status code for failed payment, but got {response.status_code}. Response: {response.text}"
    
    response_json = response.json()

    assert "transactionId" not in response_json, \
        "Response body must NOT contain 'transactionId' for failed payments"
    
    # Optionally, verify that the response includes an error message or code
    assert "error" in response_json or "message" in response_json, \
        "Response should contain an error message or details for a failed payment"
    
    # In a more comprehensive test, you would also verify that no transaction record
    # with an ID was created in the system for this failed attempt.
