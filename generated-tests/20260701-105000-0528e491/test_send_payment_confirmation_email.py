import os
import requests
import pytest
import uuid # For unique transaction IDs

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# Placeholder for the actual payment endpoint.
# This should be confirmed against the real API specification.
PAYMENT_ENDPOINT = "/api/v1/payments"

# Placeholder for a hypothetical endpoint to check sent emails in a test environment.
# In a real scenario, this might be an actual mail testing service (e.g., Mailhog API)
# or a test-specific endpoint provided by the SUT to inspect outbound email attempts.
EMAIL_LOG_ENDPOINT = "/api/v1/email-service/sent-emails"

# --- Common data for tests ---
TEST_USER_EMAIL = "test_user@example.com"
TEST_USER_PASSWORD = "securepassword123" # Not directly used for payment, but for auth
TEST_PAYMENT_AMOUNT_SUCCESS = 100.00
TEST_PAYMENT_AMOUNT_FAIL = 0.01 # Or specific card/amount to trigger failure
SUCCESS_CARD_TOKEN = "test_card_success_token" # Represents a token from a payment gateway
FAIL_CARD_TOKEN = "test_card_fail_token" # Represents a token that triggers failure

# --- Helper functions (can be converted to fixtures if needed for complex setups) ---

def authenticate_user():
    """
    Simulates user authentication and returns necessary headers/tokens.
    For this example, we'll return an empty dict. In a real scenario, this
    would involve a login POST request to get an auth token.
    """
    # Example: login_data = {"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
    # response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
    # response.raise_for_status()
    # return {"Authorization": f"Bearer {response.json()['token']}"}
    return {} # For simplicity, assuming no specific auth header is strictly required for this test scenario

def get_sent_emails(transaction_id=None):
    """
    Hypothetical function to retrieve sent emails from a test email log endpoint.
    Filters by transaction_id if provided. Raises HTTPError for bad responses.
    """
    params = {}
    if transaction_id:
        params["transaction_id"] = transaction_id

    response = requests.get(f"{BASE_URL}{EMAIL_LOG_ENDPOINT}", params=params)
    response.raise_for_status()
    return response.json()


class TestPaymentConfirmationEmails:

    @pytest.fixture(scope="class", autouse=True)
    def setup_test_environment(self):
        """
        Fixture to simulate clearing the email log or any other necessary setup
        for a clean test state before the class runs.
        """
        # Placeholder: In a real system, you might call an admin endpoint
        # to clear email logs or reset specific test data.
        print("\n--- Test setup: Ensuring a clean email log state (simulated) ---")
        yield
        print("--- Test teardown: Cleaning up after tests (simulated) ---")

    def test_confirmation_email_sent_on_successful_payment(self):
        """
        Verifies that a confirmation email is sent to the user upon a successful payment.
        """
        headers = authenticate_user()
        transaction_id = str(uuid.uuid4()) # Generate a unique ID for this transaction

        payment_data = {
            "amount": TEST_PAYMENT_AMOUNT_SUCCESS,
            "currency": "USD",
            "card_token": SUCCESS_CARD_TOKEN,
            "user_email": TEST_USER_EMAIL,
            "transaction_id": transaction_id # Pass a unique ID to easily track the email
        }

        print(f"Submitting successful payment for transaction_id: {transaction_id}")
        response = requests.post(f"{BASE_URL}{PAYMENT_ENDPOINT}", headers=headers, json=payment_data)

        assert response.status_code == 200, \
            f"Expected status code 200 for successful payment, got {response.status_code}. Response: {response.text}"

        response_json = response.json()
        assert response_json.get("status") == "success", \
            f"Expected payment status 'success', got {response_json.get('status')}. Response: {response.text}"
        assert response_json.get("transaction_id") == transaction_id, \
            f"Expected transaction ID {transaction_id}, got {response_json.get('transaction_id')}. Response: {response.text}"

        # In a real test, for async operations, you might need a short delay or polling mechanism
        # import time; time.sleep(1) # Consider polling instead of fixed sleep for robustness

        print(f"Checking email logs for transaction_id: {transaction_id}")
        sent_emails = get_sent_emails(transaction_id=transaction_id)

        assert len(sent_emails) == 1, \
            f"Expected 1 confirmation email for transaction {transaction_id}, but found {len(sent_emails)}. Emails: {sent_emails}"

        confirmation_email = sent_emails[0]
        assert confirmation_email.get("recipient") == TEST_USER_EMAIL, \
            f"Expected recipient {TEST_USER_EMAIL}, got {confirmation_email.get('recipient')}. Email: {confirmation_email}"
        assert "Payment Confirmation" in confirmation_email.get("subject", ""), \
            f"Expected 'Payment Confirmation' in email subject, got {confirmation_email.get('subject')}. Email: {confirmation_email}"
        assert f"Your payment of ${TEST_PAYMENT_AMOUNT_SUCCESS:.2f} was successful" in confirmation_email.get("body", ""), \
            f"Expected specific content in email body. Email: {confirmation_email}"
        assert confirmation_email.get("transaction_id") == transaction_id, \
            f"Email's transaction_id does not match: {confirmation_email.get('transaction_id')}. Email: {confirmation_email}"


    def test_no_confirmation_email_sent_on_failed_payment(self):
        """
        Verifies that no confirmation email is sent when a payment fails.
        """
        headers = authenticate_user()
        transaction_id = str(uuid.uuid4()) # Generate a unique ID for this transaction

        payment_data = {
            "amount": TEST_PAYMENT_AMOUNT_FAIL, # Amount that might trigger a failure
            "currency": "USD",
            "card_token": FAIL_CARD_TOKEN, # Card token designed to fail
            "user_email": TEST_USER_EMAIL,
            "transaction_id": transaction_id
        }

        print(f"Submitting failed payment for transaction_id: {transaction_id}")
        response = requests.post(f"{BASE_URL}{PAYMENT_ENDPOINT}", headers=headers, json=payment_data)

        # Assuming a failed payment might return a 400 (Bad Request), 402 (Payment Required),
        # or a 200 OK with a 'failed' status in the body. Adjust based on API specification.
        assert response.status_code in [400, 402, 200], \
            f"Expected status code 400/402 or 200 with error, got {response.status_code}. Response: {response.text}"

        response_json = response.json()
        # Check for explicit 'failed' status or a non-200 status code indicating failure
        assert response_json.get("status") == "failed" or response.status_code != 200, \
            f"Expected payment status 'failed' or non-200, got {response_json.get('status')} and code {response.status_code}. Response: {response.text}"
        assert response_json.get("transaction_id") == transaction_id, \
            f"Expected transaction ID {transaction_id}, got {response_json.get('transaction_id')}. Response: {response.text}"

        # In a real test, for async operations, you might need a short delay or polling mechanism
        # import time; time.sleep(1) # Consider polling instead of fixed sleep for robustness

        print(f"Checking email logs for transaction_id: {transaction_id}")
        sent_emails = get_sent_emails(transaction_id=transaction_id)

        assert len(sent_emails) == 0, \
            f"Expected 0 confirmation emails for failed transaction {transaction_id}, but found {len(sent_emails)}. Emails: {sent_emails}"
