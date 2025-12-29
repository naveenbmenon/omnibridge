from fastapi.testclient import TestClient
from omnibridge.main import app

client = TestClient(app)


def test_fetch_gmail_messages_requires_authentication():
    response = client.get("/sources/gmail/messages")
    assert response.status_code == 401

def test_fetch_gmail_messages_fails_if_account_not_linked():
    token_response = client.post(
        "/auth/token", params={"email": "user@example.com"}
    )
    token = token_response.json()["access_token"]

    response = client.get(
        "/sources/gmail/messages",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400


def test_fetch_gmail_messages_success(mocker):
    token_response = client.post(
        "/auth/token", params={"email": "user@example.com"}
    )
    token = token_response.json()["access_token"]

    # Link a fake Google account
    client.post(
        "/accounts/link",
        json={
            "provider": "google",
            "provider_account_id": "user@gmail.com",
            "access_token": "fake-access",
            "refresh_token": "fake-refresh",
            "expires_in": 3600,
            "scopes": ["gmail.readonly"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    mocker.patch(
        "omnibridge.api.sources.gmail_connector.fetch",
        return_value=[
            {
                "id": "msg-1",
                "source": "gmail",
                "from": "alice@example.com",
                "to": ["user@example.com"],
                "subject": "Invoice",
                "snippet": "Please see attached",
                "timestamp": "2025-02-05T10:30:00Z",
            }
        ],
    )

    response = client.get(
        "/sources/gmail/messages",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()[0]["source"] == "gmail"


