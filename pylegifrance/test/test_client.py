import os
import pytest
import requests
from dotenv import load_dotenv
from pylegifrance.client import LegifranceClient
from pylegifrance.models.consult import GetArticle
from pylegifrance.config import ApiConfig


@pytest.fixture
def api_client():
    """Fixture to provide a configured LegifranceClient client."""
    load_dotenv()
    config = ApiConfig.from_env()
    client = LegifranceClient(config=config)
    yield client
    client.close()  # Ensure the session is closed after the test


def test_client_initialization_with_env_vars():
    """
    Test that the client correctly initializes with environment variables.
    """
    # Given environment variables are set
    load_dotenv()
    client_id = os.getenv("LEGIFRANCE_CLIENT_ID")
    client_secret = os.getenv("LEGIFRANCE_CLIENT_SECRET")

    # When a client is created using environment variables
    client = LegifranceClient()  # Should load from environment variables by default

    # Then the client should have the correct API keys
    assert client.client_id == client_id
    assert client.client_secret == client_secret


def test_client_initialization_with_explicit_config():
    """
    Test that the client correctly initializes with an explicit configuration.
    """
    # Given explicit API credentials
    test_client_id = "test_client_id"
    test_client_secret = "test_client_secret"

    # Create a configuration with explicit values
    config = ApiConfig(client_id=test_client_id, client_secret=test_client_secret)

    # When a client is created with the explicit configuration
    client = LegifranceClient(config=config)

    # Then the client should have the correct API keys
    assert client.client_id == test_client_id
    assert client.client_secret == test_client_secret


def test_client_initialization_without_env_vars(monkeypatch):
    """
    Test that the client raises an error when environment variables are not set.
    """
    # Given no environment variables
    monkeypatch.delenv("LEGIFRANCE_CLIENT_ID", raising=False)
    monkeypatch.delenv("LEGIFRANCE_CLIENT_SECRET", raising=False)

    # When a client is created without explicit configuration
    # Then it should raise a ValueError
    with pytest.raises(ValueError) as excinfo:
        LegifranceClient()

    # Verify the error message
    assert "Required environment variables" in str(excinfo.value)


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

def test_multiple_client_instances():
    """
    Test that multiple client instances can be created with different configurations.
    """
    # Given two different configurations
    config1 = ApiConfig(client_id="client1", client_secret="secret1")
    config2 = ApiConfig(client_id="client2", client_secret="secret2")

    # When two clients are created with different configurations
    client1 = LegifranceClient(config=config1)
    client2 = LegifranceClient(config=config2)

    # Then they should have different configurations
    assert client1.client_id == "client1"
    assert client1.client_secret == "secret1"
    assert client2.client_id == "client2"
    assert client2.client_secret == "secret2"

    # And they should be different instances
    assert client1 is not client2

    # Clean up
    client1.close()
    client2.close()


def test_factory_method():
    """
    Test the factory method for creating client instances.
    """
    # Given a configuration
    config = ApiConfig(client_id="test_client", client_secret="test_secret")

    # When a client is created using the factory method
    client = LegifranceClient.create(config=config)

    # Then it should have the correct configuration
    assert client.client_id == "test_client"
    assert client.client_secret == "test_secret"

    # Clean up
    client.close()


def test_session_context_manager():
    """
    Test the session context manager.
    """
    # Given a client
    config = ApiConfig(client_id="test_client", client_secret="test_secret")

    # When using the client with a context manager
    with LegifranceClient(config=config).session_context() as client:
        # Then the client should be usable
        assert client.client_id == "test_client"
        assert client.client_secret == "test_secret"

    # The session should be closed after the context manager exits
    # (This is hard to test directly, but at least we can verify the context manager works)
