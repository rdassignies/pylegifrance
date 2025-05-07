import requests
import time
import os
import logging
from dotenv import load_dotenv

import yaml
from importlib import resources
from tenacity import retry, stop_after_attempt, wait_fixed, RetryError

load_dotenv()

# Lecture de la configuration à partir du fichier config.yaml
with resources.files("pylegifrance").joinpath("config.yaml").open("r") as file:
    config = yaml.safe_load(file)

logging_level = config["logging"]["level"]
logging.basicConfig(
    level=logging_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class LegiHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):
        """
        Initialisation interne de l'instance unique.

        Returns
        -------
        LegiHandler.

        """
        self.client_id = None
        self.client_secret = None
        self.token = ""
        self.token_url = "https://oauth.piste.gouv.fr/api/oauth/token"
        self.api_url = "https://api.piste.gouv.fr/dila/legifrance/lf-engine-app/"
        self.time_token = None
        self.expires_in = None

    def set_api_keys(self, legifrance_api_key=None, legifrance_api_secret=None):
        """
        Définit ou met à jour les clés API pour l'instance.

        Si les clés ne sont pas fournies, la méthode utilise les valeurs
        actuelles, si elles existent.
        Si les valeurs actuelles n'existent pas, elle tente de les
        récupérer à partir des variables d'environnement.

        Parameters
        ----------
        legifrance_api_key : str, optional
            Clé API Legifrance. Si None, conserve la valeur actuelle
            ou tente de la récupérer depuis la variable d'environnement.
        legifrance_api_secret : str, optional
            Secret API Legifrance. Si None, conserve la valeur actuelle
            ou tente de le récupérer depuis la variable d'environnement.
        """
        # Utiliser les clés existantes si de nouvelles clés ne sont pas fournies
        if legifrance_api_key is None:
            legifrance_api_key = (
                self.client_id if self.client_id else os.getenv("LEGIFRANCE_CLIENT_ID")
            )
        if legifrance_api_secret is None:
            legifrance_api_secret = (
                self.client_secret
                if self.client_secret
                else os.getenv("LEGIFRANCE_CLIENT_SECRET")
            )

        if not legifrance_api_key or not legifrance_api_secret:
            raise ValueError("Les clés de l'API Legifrance ne sont pas présentes")

        # Vérifie si les nouvelles clés sont différentes des clés existantes
        if (
            self.client_id != legifrance_api_key
            or self.client_secret != legifrance_api_secret
        ):
            self.client_id = legifrance_api_key
            self.client_secret = legifrance_api_secret
            self._get_access()  # Renouveler le token uniquement si les clés ont changé

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

        response = requests.post(self.token_url, data=data)
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
            response = requests.post(
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
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Accept": "text/plain",
                "Content-Type": "application/json",
            }
            response = requests.get(f"{self.api_url}{route}", headers=headers)
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
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        self.data = response.json()
        logger.info(f"GET request successful for URL: {url}")
        return response
