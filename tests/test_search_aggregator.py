from fastapi.testclient import TestClient
from omnibridge.main import app

client = TestClient(app)


def test_search_requires_authentication():
    response = client.get("/search?q=invoice")
    assert response.status_code == 401

def test_search_returns_empty_if_no_sources_linked():
    token_response = client.post(
        "/auth/token", params={"email": "user@example.com"}
    )
    token = token_response.json()["access_token"]

    response = client.get(
        "/search?q=invoice",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_search_aggregates_gmail_results(mocker):
    token_response = client.post(
        "/auth/token", params={"email": "user@example.com"}
    )
    token = token_response.json()["access_token"]

    # Link Gmail
    client.post(
        "/accounts/link",
        json={
            "provider": "google",
            "provider_account_id": "user@gmail.com",
            "access_token": "fake",
            "refresh_token": "fake",
            "expires_in": 3600,
            "scopes": ["gmail.readonly"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    mocker.patch(
        "omnibridge.api.search.gmail_connector.fetch",
        return_value=[
            {
                "id": "msg-1",
                "source": "gmail",
                "title": "Invoice",
                "snippet": "Payment due",
                "timestamp": "2025-02-05T10:30:00Z",
            }
        ],
    )

    response = client.get(
        "/search?q=invoice",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["source"] == "gmail"


def test_search_aggregates_multiple_sources(mocker):
    token_response = client.post(
        "/auth/token", params={"email": "user@example.com"}
    )
    token = token_response.json()["access_token"]

    mocker.patch(
        "omnibridge.api.search.gmail_connector.fetch",
        return_value=[
            {"id": "g1", "source": "gmail"}
        ],
    )

    mocker.patch(
        "omnibridge.api.search.drive_connector.fetch",
        return_value=[
            {"id": "d1", "source": "drive"}
        ],
    )

    response = client.get(
        "/search?q=test",
        headers={"Authorization": f"Bearer {token}"},
    )

    data = response.json()
    sources = {item["source"] for item in data}

    assert sources == {"gmail", "drive"}


def test_search_respects_sources_filter(mocker):
    token_response = client.post(
        "/auth/token", params={"email": "user@example.com"}
    )
    token = token_response.json()["access_token"]

    mocker.patch(
        "omnibridge.api.search.gmail_connector.fetch",
        return_value=[{"id": "g1", "source": "gmail"}],
    )

    response = client.get(
        "/search?q=test&sources=gmail",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert all(item["source"] == "gmail" for item in response.json())


