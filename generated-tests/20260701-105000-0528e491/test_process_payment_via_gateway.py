import os
import requests
import pytest

# Base URL for the API, read from environment variable or default to localhost
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# Placeholder for API endpoint - confirm with actual API spec
# In a real scenario, replace "/api/v1/payments" with the exact path.
PAYMENTS_ENDPOINT = f"{BASE_URL}/api/v1/payments"

# Placeholder for authentication token/header if required.
# In a real scenario, this would likely come from a pytest fixture
# that handles user authentication and token retrieval.
AUTH_HEADERS = {"Authorization": "Bearer YOUR_AUTH_TOKEN_HERE"}

# It's good practice to have a fixture for client sessions if many tests use them
# @pytest.fixture(scope="module")
# def api_client():
#     with requests.Session() as session:
#         session.headers.update(AUTH_HEADERS) # Apply auth if needed globally
#         yield session

def test_payment_successfully_transmitted_to_gateway():
    """
    Verifies that a valid payment request is successfully processed by the API,
    and the API returns a 200 OK status, confirming the initiation of external
    processing by the payment gateway.
    """
    # Step 1: Authenticate a user (represented by AUTH_HEADERS)
    # Step 2: Submit a valid payment request including all mandatory details.
    #         For mocking gateway success, the backend should be configured
    #         to interpret this data as a successful transaction with its mock gateway.
    valid_payment_data = {
        "amount": 100.50,
        "currency": "USD",
        "card_number": "4111222233334444",  # A test card number typically configured for success
        "expiration_month": "12",
        "expiration_year": "2025",
        "cvv": "123",
        "billing_address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip": "90210",
            "country": "USA"
        }
    }

    headers = {**AUTH_HEADERS, "Content-Type": "application/json"}
    response = requests.post(PAYMENTS_ENDPOINT, json=valid_payment_data, headers=headers)

    # Step 3 & Expected Result: API returns 200 OK and confirms processing initiation.
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}: {response.text}"

    # Assertions on response body if API provides transaction details
    response_json = response.json()
    assert "transaction_id" in response_json, "Response body should contain 'transaction_id'"
    assert response_json.get("status") == "initiated", \
        f"Expected status 'initiated' but got '{response_json.get('status')}'"

def test_payment_transmission_fails_due_to_gateway_error():
    """
    Verifies that when the API attempts to transmit payment details to the gateway
    and the gateway responds with an error (e.g., connection issue or timeout),
    the API returns an appropriate error status (500 Internal Server Error or 503 Service Unavailable).
    """
    # Step 1: Authenticate a user (represented by AUTH_HEADERS)
    # Step 2: Submit a payment request. For mocking gateway failure, the backend
    #         should be configured (e.g., via a specific test card number or header)
    #         to simulate a gateway error.
    payment_data_for_gateway_error = {
        "amount": 50.00,
        "currency": "EUR",
        "card_number": "9999888877776666",  # A test card number configured to simulate a gateway error
        "expiration_month": "10",
        "expiration_year": "2024",
        "cvv": "456",
        "billing_address": {
            "street": "456 Oak Ave",
            "city": "Otherville",
            "state": "NY",
            "zip": "10001",
            "country": "USA"
        }
    }

    headers = {**AUTH_HEADERS, "Content-Type": "application/json"}
    response = requests.post(PAYMENTS_ENDPOINT, json=payment_data_for_gateway_error, headers=headers)

    # Step 3 & Expected Result: API returns 500 or 503 status.
    assert response.status_code in [500, 503], \
        f"Expected status 500 or 503 but got {response.status_code}: {response.text}"

    # Assertions on error message in response body if available
    if response.status_code in [500, 503]:
        response_json = response.json()
        assert "error" in response_json, "Response body should contain an 'error' field"
        # Check for keywords indicating a gateway-related issue
        error_message = response_json.get("error", "").lower()
        assert any(keyword in error_message for keyword in ["gateway", "payment provider", "external service", "timeout", "unavailable"]), \
            f"Error message '{error_message}' did not contain expected gateway failure keywords."
