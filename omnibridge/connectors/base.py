from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseConnector(ABC):
    provider: str

    def __init__(self, token_store):
        self.token_store = token_store

    @abstractmethod
    def fetch(
        self,
        user_id: str,
        query: str | None = None,
        options: Dict[str, Any] | None = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch data for a given user from this provider.

        - Must use token_store internally
        - Must NOT expose tokens
        - Must return normalized data
        """
        pass
