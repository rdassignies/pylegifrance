import os
import pytest
import requests
from dotenv import load_dotenv
from pylegifrance.client.api import LegiHandler
from pylegifrance.models.consult import GetArticle


@pytest.fixture
def api_client():
    """Fixture to provide a configured LegiHandler client."""
    load_dotenv()
    client = LegiHandler()
    client.set_api_keys()
    return client


def test_client_initialization_with_env_vars(monkeypatch):
    """
    Test that the client correctly initializes with environment variables.
    """
    # Given environment variables are set
    load_dotenv()
    client_id = os.getenv("LEGIFRANCE_CLIENT_ID")
    client_secret = os.getenv("LEGIFRANCE_CLIENT_SECRET")

    # When a client is created and keys are set
    client = LegiHandler()
    client.set_api_keys()

    # Then the client should have the correct API keys
    assert client.client_id == client_id
    assert client.client_secret == client_secret

    # When environment variables are removed
    monkeypatch.delenv("LEGIFRANCE_CLIENT_ID", raising=False)
    monkeypatch.delenv("LEGIFRANCE_CLIENT_SECRET", raising=False)

    # Then the client should still retain its keys
    assert client.client_id == client_id
    assert client.client_secret == client_secret


def test_client_initialization_without_env_vars(monkeypatch):
    """
    Test that the client handles missing environment variables gracefully.
    """
    # Given a client instance
    client = LegiHandler()

    # When environment variables are removed and new keys are set to None
    monkeypatch.delenv("LEGIFRANCE_CLIENT_ID", raising=False)
    monkeypatch.delenv("LEGIFRANCE_CLIENT_SECRET", raising=False)

    # Create a new client with explicit None values to override the singleton
    client.client_id = None
    client.client_secret = None

    # Then the client should have None API keys
    assert client.client_id is None
    assert client.client_secret is None

    # When environment variables are set and keys are loaded
    load_dotenv()
    client.set_api_keys()

    # Then the client should have the correct API keys
    assert client.client_id == os.getenv("LEGIFRANCE_CLIENT_ID")
    assert client.client_secret == os.getenv("LEGIFRANCE_CLIENT_SECRET")


def test_simple_api_request(api_client):
    """
    Test that a simple API request works correctly.
    """
    # Given a valid article ID
    article_id = "LEGIARTI000047362226"
    article = GetArticle(id=article_id)

    # When the API is called
    response = api_client.call_api(
        route=article.route, data=article.model_dump(mode="json")
    )

    # Then the response should be successful
    assert response is not None


def test_api_request_with_manual_token(api_client):
    """
    Test that an API request with a manually obtained token works correctly.
    """
    # Given a client with API keys
    client = api_client

    # When a token is manually obtained
    data = {
        "grant_type": "client_credentials",
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "scope": "openid",
    }
    response_tok = requests.post(client.token_url, data=data)
    client.token = response_tok.json().get("access_token")

    # Then the token should be valid
    assert client.token is not None

    # When an API request is made with the token
    article = GetArticle(id="LEGIARTI000047362226")
    headers = {
        "Authorization": f"Bearer {client.token}",
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    url = client.api_url + article.route
    response = requests.post(url, headers=headers, json=article.model_dump(mode="json"))

    # Then the request should be successful
    assert response.status_code == 200


def test_ping_success(api_client):
    """
    Test that the ping method correctly verifies API connectivity.
    """
    # Given a configured client
    client = api_client

    # When the ping method is called
    success = client.ping()

    # Then it should return True for a valid connection
    assert success is True, "Ping should return True for a valid API connection."
