import os
import requests
import pytest

# Base URL for the API, read from environment variable or default to localhost
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# Placeholder for the payment initiation endpoint
# This path should be confirmed against the actual API specification.
PAYMENT_INITIATE_ENDPOINT = "/api/v1/payments/initiate"

# --- Helper Functions (Simulated for testing purposes) ---

def get_valid_auth_token():
    """
    Simulates obtaining a valid authentication token.
    In a real test scenario, this would involve:
    1. Registering/logging in a test user.
    2. Extracting the token (e.g., from login response).
    3. Potentially storing it for subsequent requests.
    For this example, we use a static placeholder token.
    """
    # Replace with logic to get a real token if an auth endpoint is available
    return "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsImlhdCI6MTY3ODAwMDAwMH0.signature_placeholder"

# --- Test Cases ---

def test_authenticated_user_initiates_payment():
    """
    Verifies that an authenticated user can successfully initiate a payment.
    Expects a 200 OK or 302 Redirect status for successful processing or gateway redirect.
    """
    token = get_valid_auth_token()
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payment_details = {
        "amount": 100.00,
        "currency": "USD",
        "payment_method": "credit_card",
        "user_id": 123  # Assuming user_id is part of details or derived from token
    }

    print(f"\nAttempting payment initiation with token: {token[:30]}...")
    print(f"Sending POST to: {BASE_URL}{PAYMENT_INITIATE_ENDPOINT}")

    try:
        response = requests.post(
            f"{BASE_URL}{PAYMENT_INITIATE_ENDPOINT}",
            headers=headers,
            json=payment_details
        )
    except requests.exceptions.ConnectionError as e:
        pytest.fail(f"API connection error: {e}. Ensure {BASE_URL} is running.")

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

    # Expect 200 OK for successful processing or 302 Redirect to payment gateway
    assert response.status_code in [200, 302], \
        f"Expected status 200 or 302 for authenticated payment, got {response.status_code}. Response: {response.text}"
    
    # Further assertions could check response body for payment ID, redirect URL, etc.
    if response.status_code == 200:
        assert "payment_id" in response.json(), "Response body should contain 'payment_id' for 200 OK"
        assert response.json()["status"] == "initiated", "Payment status should be 'initiated'"
    elif response.status_code == 302:
        assert "Location" in response.headers, "Redirect response should have 'Location' header"

def test_unauthenticated_user_initiates_payment_fails():
    """
    Verifies that an unauthenticated user cannot initiate a payment.
    Expects a 401 Unauthorized status.
    """
    payment_details = {
        "amount": 50.00,
        "currency": "EUR",
        "payment_method": "paypal",
        "user_id": 456
    }

    print(f"\nAttempting payment initiation without authentication token.")
    print(f"Sending POST to: {BASE_URL}{PAYMENT_INITIATE_ENDPOINT}")

    try:
        response = requests.post(
            f"{BASE_URL}{PAYMENT_INITIATE_ENDPOINT}",
            json=payment_details
        )
    except requests.exceptions.ConnectionError as e:
        pytest.fail(f"API connection error: {e}. Ensure {BASE_URL} is running.")

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

    assert response.status_code == 401, \
        f"Expected status 401 for unauthenticated payment, got {response.status_code}. Response: {response.text}"
    
    # Further assertions could check for specific error messages
    try:
        error_message = response.json().get("message")
        assert "Authentication required" in error_message or \
               "Unauthorized" in error_message or \
               "Missing authentication token" in error_message,
               f"Expected an authentication error message, got '{error_message}'"
    except requests.exceptions.JSONDecodeError:
        # If the response isn't JSON, just check the status code
        pass
