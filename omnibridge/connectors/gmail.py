from typing import Any, Dict, List
from datetime import datetime, timezone

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from omnibridge.connectors.base import BaseConnector
from omnibridge.accounts.models import Account


class GmailConnector(BaseConnector):
    provider = "google"

    def fetch(
        self,
        user_id: str,
        query: str | None = None,   # query intentionally ignored in v1
        options: Dict[str, Any] | None = None,
    ) -> List[Dict[str, Any]]:
        

        account = self.token_store.get_account(user_id, self.provider)

        if not account:
            raise Exception("Google account not linked")

        messages = self._fetch_from_gmail_api(account)

        normalized: List[Dict[str, Any]] = []
        for message in messages:
            message["source"] = "gmail"
            normalized.append(message)

        return normalized

    def _fetch_from_gmail_api(
        self,
        account: Account,
        max_results: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Fetch recent Gmail messages using real Gmail API.
        Query is intentionally ignored in v1 for reliability.
        """

        # 1️⃣ Build Google credentials from stored access token
        creds = Credentials(token=account.access_token)

        # 2️⃣ Create Gmail API client
        service = build("gmail", "v1", credentials=creds)

        

        # 4️⃣ Fetch most recent messages (no Gmail search filter)
        response = service.users().messages().list(
            userId="me",
            maxResults=max_results,
            includeSpamTrash=True,
        ).execute()

        

        messages = response.get("messages", [])
        results: List[Dict[str, Any]] = []

        for msg in messages:
            msg_detail = service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="metadata",
                metadataHeaders=["From", "To", "Subject", "Date"],
            ).execute()

            headers = {
                h["name"]: h["value"]
                for h in msg_detail.get("payload", {}).get("headers", [])
            }

            results.append({
                "id": msg_detail["id"],
                "from": headers.get("From"),
                "to": headers.get("To", "").split(",") if headers.get("To") else [],
                "subject": headers.get("Subject"),
                "snippet": msg_detail.get("snippet"),
                "timestamp": self._parse_date(headers.get("Date")),
            })

        return results

    def _parse_date(self, date_str: str | None) -> str | None:
        """
        Parse Gmail date header into ISO 8601 format.
        """
        if not date_str:
            return None

        try:
            # Example: "Mon, 15 Jan 2024 12:34:56 +0530"
            dt = datetime.strptime(date_str[:25], "%a, %d %b %Y %H:%M:%S")
            return dt.replace(tzinfo=timezone.utc).isoformat()
        except Exception:
            return None
