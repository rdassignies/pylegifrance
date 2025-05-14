import requests
import time
import logging
from typing import Optional, ClassVar, Self
from contextlib import contextmanager
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed, RetryError
from pylegifrance.config import ApiConfig

load_dotenv()

logger = logging.getLogger(__name__)


class LegifranceClient:
    """
    Client for interacting with the Legifrance API.

    This class provides methods for authenticating with the API and making requests.
    It can be instantiated directly or created using the factory methods.

    Attributes:
        client_id: The client ID for the Legifrance API.
        client_secret: The client secret for the Legifrance API.
        token: The current access token.
        token_url: The URL for obtaining access tokens.
        api_url: The base URL for the Legifrance API.
        time_token: The timestamp when the token was obtained.
        expires_in: The token expiration time in seconds.
        session: The requests session used for making API calls.
    """
    # Class variable to store the default instance for backward compatibility
    _default_instance: ClassVar[Optional['LegifranceClient']] = None

    def __init__(self, config=None):
        """
        Initialize a new LegifranceClient instance.

        Parameters
        ----------
        config : ApiConfig, optional
            Configuration for the API client. If None, will attempt to load from environment variables.

        Raises
        ------
        ValueError
            If config is not provided and environment variables are not set.
        """
        if config is None:
            try:
                config = ApiConfig.from_env()
            except ValueError as e:
                logger.error(f"Failed to initialize API client: {e}")
                raise

        self.client_id = config.client_id
        self.client_secret = config.client_secret
        self.token = ""
        self.token_url = config.token_url
        self.api_url = config.api_url
        self.time_token = None
        self.expires_in = None
        self.session = requests.Session()

    def set_api_keys(self, client_id=None, client_secret=None):
        """
        Définit ou met à jour les clés API pour l'instance.

        Si les clés sont fournies, elles remplacent les valeurs actuelles.
        Si les clés ne sont pas fournies, la méthode tente de les récupérer
        à partir des variables d'environnement.

        Parameters
        ----------
        client_id : str, optional
            Clé API Legifrance. Si None, tente de la récupérer depuis
            la variable d'environnement.
        client_secret : str, optional
            Secret API Legifrance. Si None, tente de le récupérer depuis
            la variable d'environnement.

        Raises
        ------
        ValueError
            Si les clés ne sont pas fournies et ne peuvent pas être récupérées
            depuis les variables d'environnement.
        """
        if client_id is not None and client_secret is not None:
            # Use provided keys
            new_config = ApiConfig(client_id=client_id, client_secret=client_secret)
        else:
            # Try to load from environment
            try:
                new_config = ApiConfig.from_env()
            except ValueError as e:
                logger.error(f"Failed to set API keys: {e}")
                raise

        # Check if keys have changed
        if (
            self.client_id != new_config.client_id
            or self.client_secret != new_config.client_secret
        ):
            self.client_id = new_config.client_id
            self.client_secret = new_config.client_secret
            self._get_access()  # Refresh token only if keys have changed

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5), reraise=True)
    def _get_access(self):
        """
        Obtention du jeton d'accès avec récupération et log des éventuelles erreurs.
        Utilise la bibliothèque tenacity pour gérer les tentatives.
        """
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "openid",
        }

        response = self.session.post(self.token_url, data=data)
        if 200 <= response.status_code < 300:
            token = response.json().get("access_token")
            self.time_token = time.time()
            self.token = token
            self.expires_in = response.json().get("expires_in")
            logger.info("Legifrance API connection successful.")
        else:
            logger.warning(
                f"Failed to get token: {response.status_code} - {response.text}"
            )
            raise Exception(
                f"Error obtaining token: {response.status_code} - {response.text}"
            )

    def _update_client(self):
        """
        Fonction qui renouvelle le token si besoin
        """
        if self.time_token is None or self.expires_in is None:
            try:
                self._get_access()
            except RetryError as exc:
                logger.error(f"Could not obtain access token after retries: {exc}")
                raise
            return

        elapsed_time = time.time() - self.time_token
        if elapsed_time >= self.expires_in:
            logger.info("Token expired, renewing access token.")
            try:
                self._get_access()
            except RetryError as exc:
                logger.error(f"Could not refresh access token after retries: {exc}")
                raise

    def call_api(self, route: str, data: str):
        """
        Appel à l'API Legifrance avec gestion du token et journalisation des erreurs.

        Parameters
        ----------
        route : str
            La route de l'API à utiliser.
        data : str
            Les données à envoyer au format JSON.

        Returns
        -------
        requests.Response
            La réponse de l'API.
        """
        self._update_client()
        headers = {
            "Authorization": f"Bearer {self.token}",
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        if data is not None:
            response = self.session.post(
                f"{self.api_url}{route}", headers=headers, json=data
            )
        else:
            logger.warning("No data provided to call_api; request not sent.")
            raise ValueError("No data provided for API call.")

        if 400 <= response.status_code < 600:
            logger.error(
                f"Client error {response.status_code} - {response.text} when calling the API."
            )
            raise Exception(
                f"Erreur client {response.status_code} - {response.text} lors de l'appel à l'API :"
            )

        logger.info(f"API call to '{route}' successful.")
        return response

    def ping(self, route: str = "consult/ping"):
        """
        Vérifie la connectivité avec l'API Legifrance en envoyant une requête ping.

        Parameters
        ----------
        route : str, optional
            Route à utiliser pour le ping (par défaut : "consult/ping").

        Returns
        -------
        bool
            True si la connexion est réussie, sinon False.

        Raises
        ------
        Exception
            En cas d'erreur de connexion à l'API.
        """
        try:
            # Ensure we have a valid token before pinging
            self._update_client()
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Accept": "text/plain",
                "Content-Type": "application/json",
            }
            response = self.session.get(f"{self.api_url}{route}", headers=headers)
            if response.status_code == 200:
                logger.info(
                    "Ping successful: connection to Legifrance API established."
                )
                return True
            else:
                logger.warning(
                    f"Ping failed: return code {response.status_code} - {response.text}"
                )
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Error during Legifrance API ping: {str(e)}")
            raise Exception(f"Échec du ping de l'API : {e}")

    def get(self, route: str):
        """
        Effectue une requête GET sur la route donnée de l'API.

        Parameters
        ----------
        route : str
            La route à cibler.

        Returns
        -------
        requests.Response
            La réponse de l'API.
        """
        self._update_client()
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.api_url}{route}"
        logger.info(f"GET request to URL: {url}")
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        self.data = response.json()
        logger.info(f"GET request successful for URL: {url}")
        return response

    @classmethod
    def create(cls, config: Optional[ApiConfig] = None) -> Self:
        """
        Factory method to create a new LegifranceClient instance.

        Parameters
        ----------
        config : ApiConfig, optional
            Configuration for the API client. If None, will attempt to load from environment variables.

        Returns
        -------
        LegifranceClient
            A new instance of LegifranceClient.
        """
        return cls(config=config)


    @contextmanager
    def session_context(self):
        """
        Context manager for using the client in a with statement.

        This ensures that the session is properly closed after use.

        Yields
        ------
        LegifranceClient
            The client instance.
        """
        try:
            yield self
        finally:
            self.session.close()

    def close(self):
        """
        Close the client's session.

        This should be called when the client is no longer needed to free up resources.
        """
        self.session.close()
