import json
import logging
from datetime import datetime
from typing import List, Optional, Union, Dict, Any

from pylegifrance.client import LegifranceClient
from pylegifrance.models.identifier import Cid, Eli, Nor
from pylegifrance.utils import EnumEncoder

from pylegifrance.models.juri.models import Decision
from pylegifrance.models.juri.search import SearchRequest
from pylegifrance.models.juri.api_wrappers import (
    ConsultRequest,
    ConsultByAncienIdRequest,
    ConsultResponse,
)

HTTP_OK = 200
CITATION_TYPE = "CITATION"

logger = logging.getLogger(__name__)


class JuriDecision:
    """
    High-level domain object representing a judicial decision.

    This class wraps the Decision model and provides rich behaviors like
    .latest(), .citations(), .versions(), and .at(date).
    """

    def __init__(self, decision: Decision, client: LegifranceClient):
        """
        Initialize a JuriDecision instance.

        Parameters
        ----------
        decision : Decision
            The underlying Decision model.
        client : LegifranceClient
            The client for interacting with the Legifrance API.
        """
        self._decision = decision
        self._client = client

    @property
    def id(self) -> Optional[str]:
        """Get the ID of the decision."""
        return self._decision.id

    @property
    def cid(self) -> Optional[Cid]:
        """Get the CID of the decision with validation."""
        if not hasattr(self._decision, "cid") or not self._decision.cid:
            return None
        return Cid(self._decision.cid)

    @property
    def eli(self) -> Optional[Eli]:
        """Get the ELI of the decision with validation."""
        if not self._decision.id_eli:
            return None
        return Eli(self._decision.id_eli)

    @property
    def nor(self) -> Optional[Nor]:
        """Get the NOR of the decision with validation."""
        if not self._decision.nor:
            return None
        return Nor(self._decision.nor)

    @property
    def ecli(self) -> Optional[str]:
        """Get the ECLI of the decision."""
        return getattr(self._decision, "ecli", None)

    @property
    def date(self) -> Optional[datetime]:
        """Get the date of the decision."""
        if not self._decision.date_texte:
            return None

        try:
            # Handle both string and datetime types
            if isinstance(self._decision.date_texte, str):
                return datetime.fromisoformat(self._decision.date_texte)
            elif isinstance(self._decision.date_texte, datetime):
                return self._decision.date_texte
        except (ValueError, TypeError):
            # Handle case where dateTexte is not a valid ISO format
            return None
        return None

    @property
    def title(self) -> Optional[str]:
        """Get the title of the decision."""
        return self._decision.titre

    @property
    def long_title(self) -> Optional[str]:
        """Get the long title of the decision."""
        return self._decision.titre_long

    @property
    def text(self) -> Optional[str]:
        """Get the text of the decision."""
        return self._decision.texte

    @property
    def text_html(self) -> Optional[str]:
        """Get the HTML text of the decision."""
        return self._decision.texte_html

    @property
    def formation(self) -> Optional[str]:
        """Get the formation of the decision."""
        return self._decision.formation

    @property
    def numero(self) -> Optional[str]:
        """Get the number of the decision."""
        return getattr(self._decision, "num", None)

    @property
    def jurisdiction(self) -> Optional[str]:
        """Get the jurisdiction of the decision."""
        return getattr(self._decision, "juridiction", None)

    @property
    def solution(self) -> Optional[str]:
        """Get the solution of the decision."""
        return getattr(self._decision, "solution", None)

    def citations(self) -> List["JuriDecision"]:
        """
        Get the citations of the decision.

        Returns
        -------
        List[JuriDecision]
            A list of JuriDecision objects representing the citations.
        """
        citations = []
        for lien in self._decision.liens:
            if lien.type_lien != CITATION_TYPE:
                continue
            if not lien.cid_texte or lien.cid_texte == "":
                continue

            try:
                decision = JuriAPI(self._client).fetch(lien.cid_texte)
                if decision:
                    citations.append(decision)
            except Exception:
                # Skip citations that can't be fetched
                # We use a generic exception here because we want to continue processing
                # other citations even if one fails for any reason
                pass
        return citations

    def at(self, date: Union[datetime, str]) -> Optional["JuriDecision"]:
        """
        Get the version of the decision at the specified date.

        Parameters
        ----------
        date : Union[datetime, str]
            The date to get the version at.

        Returns
        -------
        Optional[JuriDecision]
            The version of the decision at the specified date, or None if not found.
        """
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date)
            except ValueError:
                raise ValueError(f"Invalid date format: {date}")

        # Convert date to ISO format string for the API
        date_str = date.isoformat()

        # Use the JuriAPI to fetch the version at the specified date
        try:
            if self.id is None:
                return None
            return JuriAPI(self._client).fetch_version_at(self.id, date_str)
        except Exception:
            return None

    def latest(self) -> Optional["JuriDecision"]:
        """
        Get the latest version of the decision.

        Returns
        -------
        Optional[JuriDecision]
            The latest version of the decision, or None if not found.
        """
        if self.id is None:
            return None

        try:
            return JuriAPI(self._client).fetch(self.id)
        except Exception:
            return None

    def versions(self) -> List["JuriDecision"]:
        """
        Get all versions of the decision.

        Returns
        -------
        List[JuriDecision]
            A list of JuriDecision objects representing all versions.
        """
        if self.id is None:
            return []

        try:
            return JuriAPI(self._client).fetch_versions(self.id)
        except Exception:
            return []

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the decision to a dictionary.

        Returns
        -------
        Dict[str, Any]
            A dictionary representation of the decision.
        """
        return self._decision.model_dump()

    def __repr__(self) -> str:
        """Get a string representation of the decision."""
        return f"JuriDecision(id={self.id}, date={self.date}, title={self.title})"


class JuriAPI:
    """
    High-level API for interacting with JURI data from the Legifrance API.
    """

    def __init__(self, client: LegifranceClient):
        """
        Initialize a JuriAPI instance.

        Parameters
        ----------
        client : LegifranceClient
            The client for interacting with the Legifrance API.
        """
        self._client = client

    def _process_consult_response(
        self, response_data: ConsultResponse
    ) -> Optional[Decision]:
        """
        Process a consult response and extract the Decision.

        Parameters
        ----------
        response_data : dict
            The JSON response data from the API.

        Returns
        -------
        Optional[Decision]
            The Decision object, or None if not found.
        """
        consult_response = ConsultResponse.from_api_model(response_data)

        if not consult_response.text:
            return None

        # Fix: Use the text data directly since it's already a dict
        if isinstance(consult_response.text, dict):
            decision_data = consult_response.text
        else:
            decision_data = consult_response.text.model_dump()

        return Decision.model_validate(decision_data)

    def fetch(self, text_id: str) -> Optional[JuriDecision]:
        """
        Fetch a decision by its ID.

        Parameters
        ----------
        text_id : str
            The ID of the decision to fetch.

        Returns
        -------
        Optional[JuriDecision]
            The decision, or None if not found.

        Raises
        ------
        ValueError
            If the text_id is invalid.
        Exception
            If the API call fails.
        """
        if not text_id:
            raise ValueError("text_id cannot be empty")

        request = ConsultRequest(textId=text_id, searchedString="")

        response = self._client.call_api(
            "consult/juri", request.to_api_model().model_dump(by_alias=True)
        )

        if response.status_code != HTTP_OK:
            return None

        response_data = response.json()
        decision = self._process_consult_response(response_data)

        if not decision:
            return None

        return JuriDecision(decision, self._client)

    def fetch_with_ancien_id(self, ancien_id: str) -> Optional[JuriDecision]:
        """
        Fetch a decision by its ancien ID.

        Parameters
        ----------
        ancien_id : str
            The ancien ID of the decision to fetch.

        Returns
        -------
        Optional[JuriDecision]
            The decision, or None if not found.
        """
        if not ancien_id:
            raise ValueError("ancien_id cannot be empty")

        request = ConsultByAncienIdRequest(ancienId=ancien_id)

        response = self._client.call_api(
            "consult/juri/ancienId",
            request.to_api_model().model_dump(by_alias=True),
        )

        if response.status_code != HTTP_OK:
            return None

        response_data = response.json()
        decision = self._process_consult_response(response_data)

        if not decision:
            return None

        return JuriDecision(decision, self._client)

    def fetch_version_at(self, text_id: str, date: str) -> Optional[JuriDecision]:
        """
        Fetch the version of a decision at a specific date.

        Parameters
        ----------
        text_id : str
            The ID of the decision to fetch.
        date : str
            The date to get the version at, in ISO format.

        Returns
        -------
        Optional[JuriDecision]
            The version of the decision at the specified date, or None if not found.
        """
        if not text_id:
            raise ValueError("text_id cannot be empty")

        try:
            datetime.fromisoformat(date)
        except ValueError:
            raise ValueError(f"Invalid date format: {date}")

        request = {"textId": text_id, "date": date}
        response = self._client.call_api("consult/juri/version", request)

        if response.status_code != HTTP_OK:
            return None

        response_data = response.json()
        decision = self._process_consult_response(response_data)

        if not decision:
            return None

        return JuriDecision(decision, self._client)

    def fetch_versions(self, text_id: str) -> List[JuriDecision]:
        """
        Fetch all versions of a decision.

        Parameters
        ----------
        text_id : str
            The ID of the decision to fetch versions for.

        Returns
        -------
        List[JuriDecision]
            A list of JuriDecision objects representing all versions.
        """
        if not text_id:
            raise ValueError("text_id cannot be empty")

        request = {"textId": text_id}
        response = self._client.call_api("consult/juri/versions", request)

        if response.status_code != HTTP_OK:
            return []

        response_data = response.json()

        if not isinstance(response_data, list):
            return []

        versions = []
        for version_data in response_data:
            decision = self._process_consult_response(version_data)
            if decision:
                versions.append(JuriDecision(decision, self._client))

        return versions

    def search(self, query: Union[str, SearchRequest]) -> List[JuriDecision]:
        """
        Search for decisions matching the query.

        Parameters
        ----------
        query : Union[str, SearchRequest]
            The search query, either as a string or a SearchRequest object.

        Returns
        -------
        List[JuriDecision]
            A list of JuriDecision objects matching the query.
        """
        if isinstance(query, str):
            search_query = SearchRequest(search=query)
        else:
            search_query = query

        request_dto = search_query.to_api_model()

        request = request_dto.model_dump(by_alias=True)
        request = json.loads(json.dumps(request, cls=EnumEncoder))

        response = self._client.call_api("search", request)

        if response.status_code != HTTP_OK:
            return []

        response_data = response.json()

        if "results" not in response_data or not isinstance(
            response_data["results"], list
        ):
            return []

        results = []
        for result in response_data["results"]:
            if (
                "titles" not in result
                or not isinstance(result["titles"], list)
                or len(result["titles"]) == 0
            ):
                continue

            title = result["titles"][0]

            if "id" not in title:
                continue

            text_id = title["id"]

            try:
                decision = self.fetch(text_id)
                if decision:
                    results.append(decision)
                    logger.debug(f"Successfully fetched and added decision {text_id}")
                else:
                    logger.warning(
                        f"Failed to fetch decision {text_id} (returned None)"
                    )
            except Exception as e:
                logger.error(f"Exception while fetching decision {text_id}: {e}")

        return results
