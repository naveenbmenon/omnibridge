from fastapi.testclient import TestClient
from omnibridge.main import app

client = TestClient(app)


def test_protected_endpoint_without_token_is_rejected():
    response = client.get("/protected")
    assert response.status_code == 401
def test_protected_endpoint_with_missing_authorization_header_is_rejected():
    response = client.get("/protected", headers={})
    assert response.status_code == 401
def test_protected_endpoint_with_malformed_authorization_header_is_rejected():
    response = client.get(
        "/protected",
        headers={"Authorization": "InvalidTokenFormat"},
    )
    assert response.status_code == 401
def test_protected_endpoint_with_empty_bearer_token_is_rejected():
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer "},
    )
    assert response.status_code == 401
def test_protected_endpoint_with_invalid_jwt_is_rejected():
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer invalid.jwt.token"},
    )
    assert response.status_code == 401
def test_issue_token_and_access_protected_endpoint():
    # 1) Issue token
    token_response = client.post("/auth/token", params={"email": "user@example.com"})
    assert token_response.status_code == 200

    token = token_response.json()["access_token"]

    # 2) Use token to access protected endpoint
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == "user@example.com"
