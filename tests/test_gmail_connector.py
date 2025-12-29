from datetime import datetime, timedelta, timezone
from omnibridge.accounts.models import Account


def make_google_account(user_id="user@example.com"):
    return Account(
        user_id=user_id,
        provider="google",
        provider_account_id="user@gmail.com",
        access_token="fake-access-token",
        refresh_token="fake-refresh-token",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        scopes=["gmail.readonly"],
        created_at=datetime.now(timezone.utc),
    )


import pytest
from omnibridge.connectors.gmail import GmailConnector
from omnibridge.accounts.store import InMemoryTokenStore


def test_gmail_connector_fails_if_account_not_linked():
    store = InMemoryTokenStore()
    connector = GmailConnector(token_store=store)

    with pytest.raises(Exception):
        connector.fetch(user_id="user@example.com")


def test_gmail_connector_uses_token_store():
    store = InMemoryTokenStore()
    store.save_account(make_google_account())

    connector = GmailConnector(token_store=store)

    # We expect failure later (API not mocked),
    # but NOT a "missing account" failure
    try:
        connector.fetch(user_id="user@example.com")
    except Exception as e:
        assert "not linked" not in str(e).lower()


def test_gmail_connector_returns_normalized_messages(mocker):
    store = InMemoryTokenStore()
    store.save_account(make_google_account())

    connector = GmailConnector(token_store=store)

    # Mock internal Gmail API call
    mocker.patch.object(
        connector,
        "_fetch_from_gmail_api",
        return_value=[
            {
                "id": "msg-1",
                "from": "alice@example.com",
                "to": ["user@example.com"],
                "subject": "Invoice",
                "snippet": "Please see attached",
                "timestamp": "2025-02-05T10:30:00Z",
            }
        ],
    )

    results = connector.fetch(user_id="user@example.com")

    assert isinstance(results, list)
    assert results[0]["source"] == "gmail"
    assert "access_token" not in results[0]

def test_gmail_connector_accepts_query(mocker):
    store = InMemoryTokenStore()
    store.save_account(make_google_account())

    connector = GmailConnector(token_store=store)

    mock = mocker.patch.object(
        connector,
        "_fetch_from_gmail_api",
        return_value=[],
    )

    connector.fetch(user_id="user@example.com", query="invoice")

    mock.assert_called_once()

