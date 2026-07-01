import os
import requests
import pytest

# Base URL from environment variable or default
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# Placeholder for the payment details endpoint
PAYMENT_DETAILS_ENDPOINT = "/api/v1/payments/details"  # Confirm with actual API spec

# Placeholder for authentication headers
# In a real scenario, this would involve logging in or using a token from a fixture.
# For this example, we'll use a mock token.
@pytest.fixture(scope="module")
def auth_headers():
    # Simulate authentication by returning headers with a valid token
    # In a real test, this would involve calling a login endpoint
    # and extracting the token from the response.
    print("\nSimulating user authentication...")
    mock_token = "mock_auth_token_12345"
    return {"Authorization": f"Bearer {mock_token}"}

class TestPaymentDetails:

    def test_submit_valid_payment_method_details(self, auth_headers):
        """
        Verifies that the API accepts and successfully processes various valid
        payment method details, returning a 200 OK for each.
        """
        print(f"\nTesting endpoint: {BASE_URL}{PAYMENT_DETAILS_ENDPOINT}")

        # Test Case 1.1: Valid Credit Card Information
        credit_card_payload = {
            "type": "credit_card",
            "card_number": "4111222233334444",
            "expiry_month": "12",
            "expiry_year": "2025",
            "cvv": "123",
            "cardholder_name": "John Doe"
        }
        print(f"Sending valid credit card payload: {credit_card_payload}")
        response_cc = requests.post(f"{BASE_URL}{PAYMENT_DETAILS_ENDPOINT}",
                                    json=credit_card_payload,
                                    headers=auth_headers)

        assert response_cc.status_code == 200
        assert response_cc.json().get("status") == "success"
        assert "Payment details processed successfully" in response_cc.json().get("message")
        print(f"Credit card processing successful. Response: {response_cc.json()}")

        # Test Case 1.2: Valid UPI ID
        upi_payload = {
            "type": "upi",
            "upi_id": "johndoe@ybl",
            "account_holder_name": "John Doe"
        }
        print(f"Sending valid UPI payload: {upi_payload}")
        response_upi = requests.post(f"{BASE_URL}{PAYMENT_DETAILS_ENDPOINT}",
                                   json=upi_payload,
                                   headers=auth_headers)

        assert response_upi.status_code == 200
        assert response_upi.json().get("status") == "success"
        assert "Payment details processed successfully" in response_upi.json().get("message")
        print(f"UPI processing successful. Response: {response_upi.json()}")

    def test_submit_unsupported_payment_method_details(self, auth_headers):
        """
        Verifies that the API rejects requests for unsupported payment method types,
        returning a 400 Bad Request status.
        """
        print(f"\nTesting endpoint: {BASE_URL}{PAYMENT_DETAILS_ENDPOINT}")

        unsupported_payload = {
            "type": "crypto_currency",
            "wallet_address": "0x123abc...",
            "currency": "BTC"
        }
        print(f"Sending unsupported payment method payload: {unsupported_payload}")
        response = requests.post(f"{BASE_URL}{PAYMENT_DETAILS_ENDPOINT}",
                                 json=unsupported_payload,
                                 headers=auth_headers)

        assert response.status_code == 400
        assert response.json().get("status") == "error"
        assert "Unsupported payment method" in response.json().get("message", "").lower() or \
               "invalid payment type" in response.json().get("message", "").lower()
        print(f"Unsupported payment method correctly rejected. Response: {response.json()}")
