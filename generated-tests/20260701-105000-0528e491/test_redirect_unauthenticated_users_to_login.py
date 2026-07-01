import os
import requests
import pytest

# Base URL for the API, read from environment variable or default to localhost
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# Placeholder for the actual API endpoint for initiating payments.
# This should be confirmed against the real API specification.
PAYMENT_INITIATE_ENDPOINT = f"{BASE_URL}/api/v1/payments/initiate"

# Placeholder for the expected login page path for redirection.
# This should be confirmed against the real API specification.
LOGIN_PAGE_PATH = "/login"


def test_unauthenticated_user_redirected_for_payment():
    """
    Verifies that an unauthenticated user attempting to initiate a payment
    is correctly redirected to the login page.
    """
    print(f"\nAttempting GET request to: {PAYMENT_INITIATE_ENDPOINT}")
    # Send a GET request without authentication, disallowing redirects
    # to inspect the 302 status and Location header.
    response = requests.get(PAYMENT_INITIATE_ENDPOINT, allow_redirects=False)

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")

    # Assert a 302 Found status code
    assert response.status_code == 302, \
        f"Expected status code 302, but got {response.status_code}"

    # Assert that a 'Location' header is present
    assert 'Location' in response.headers, \
        "Expected 'Location' header in response, but it was missing"

    # Assert that the 'Location' header points to the login page
    location_url = response.headers['Location']
    assert LOGIN_PAGE_PATH in location_url, \
        f"Expected 'Location' header to point to '{LOGIN_PAGE_PATH}', but got '{location_url}'"


def test_unauthenticated_user_accesses_payment_without_redirection():
    """
    Verifies that if the redirection logic fails, the API returns a 401 Unauthorized
    status instead of a 302, indicating an incorrect implementation.
    (This test case asserts the *absence* of the desired redirect behavior.)
    """
    print(f"\nAttempting GET request to: {PAYMENT_INITIATE_ENDPOINT}")
    # Send a GET request without authentication, disallowing redirects.
    # For this negative test, we expect a 401, not a 302 redirect.
    response = requests.get(PAYMENT_INITIATE_ENDPOINT, allow_redirects=False)

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")

    # Assert a 401 Unauthorized status code, indicating that the intended
    # redirection to login did not occur, and access was simply denied.
    assert response.status_code == 401, \
        f"Expected status code 401 (no redirect), but got {response.status_code}"

    # Additionally, ensure that there is no 'Location' header, confirming it wasn't a redirect.
    assert 'Location' not in response.headers, \
        "Did not expect 'Location' header in response, but it was present, indicating an unexpected redirect attempt."
