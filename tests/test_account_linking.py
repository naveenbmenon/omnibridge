from fastapi.testclient import TestClient
from omnibridge.main import app

client = TestClient(app)


def test_link_account_successfully():
    # Issue JWT
    token_response = client.post(
        "/auth/token", params={"email": "user@example.com"}
    )
    token = token_response.json()["access_token"]

    # Mock OAuth payload
    payload = {
        "provider": "google",
        "provider_account_id": "user@gmail.com",
        "access_token": "access-token",
        "refresh_token": "refresh-token",
        "expires_in": 3600,
        "scopes": ["gmail.readonly"],
    }

    response = client.post(
        "/accounts/link",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "linked"

def test_link_account_requires_authentication():
    response = client.post("/accounts/link", json={})

    assert response.status_code == 401


def test_link_account_does_not_return_tokens():
    token_response = client.post(
        "/auth/token", params={"email": "user@example.com"}
    )
    token = token_response.json()["access_token"]

    payload = {
        "provider": "google",
        "provider_account_id": "user@gmail.com",
        "access_token": "access-token",
        "refresh_token": "refresh-token",
        "expires_in": 3600,
        "scopes": ["gmail.readonly"],
    }

    response = client.post(
        "/accounts/link",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    body = response.json()

    assert "access_token" not in body
    assert "refresh_token" not in body


