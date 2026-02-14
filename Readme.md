# OmniBridge

A pluggable API gateway that centralizes OAuth-based access to third-party services behind a secure, unified backend interface.

## Problem

Every third-party service has its own OAuth flow, API design, and response format. Applications that integrate multiple providers end up duplicating token management, error handling, and normalization logic across their codebase.

## Solution

OmniBridge acts as a single backend gateway — handling OAuth, securely storing provider tokens, and exposing a normalized API that applications can consume without ever touching provider-specific logic directly.

## Architecture

```
Client / Application
        ↓
JWT Authentication (OmniBridge)
        ↓
OmniBridge API Layer
        ↓
Connector Layer (pluggable per provider)
        ↓
External Provider APIs (Gmail, ...)
```

**Core principle:** Applications never communicate directly with third-party APIs. OmniBridge mediates all provider interactions.

## Authentication Model

OmniBridge uses two distinct token layers:

| Token | Purpose |
|---|---|
| JWT | Identifies the user within OmniBridge |
| OAuth Access Token | Used to call provider APIs on behalf of the user |
| OAuth Refresh Token | Renews expired access tokens server-side |

- JWTs are stateless and validated on every request
- OAuth tokens are stored server-side and never exposed to clients

## Connector Architecture

OmniBridge uses a pluggable connector system. Each connector:

- Handles authentication with one specific provider
- Converts provider responses into a normalized format
- Is fully isolated from OmniBridge core logic

New providers can be added by implementing the base connector interface without modifying existing code.

**Normalized email response (Gmail Connector):**
```json
{
  "id": "string",
  "source": "gmail",
  "from": "string",
  "to": ["string"],
  "subject": "string",
  "snippet": "string",
  "timestamp": "ISO-8601"
}
```

## Project Structure

```
omnibridge_v1/
├── omnibridge/
│   ├── main.py                 # FastAPI app entry point
│   ├── api/
│   │   ├── auth_routes.py      # JWT issuing endpoints
│   │   ├── accounts.py         # Account linking & listing
│   │   └── sources.py          # Provider data access endpoints
│   ├── auth/
│   │   ├── jwt.py              # JWT creation & verification
│   │   └── dependencies.py     # Auth dependency injection
│   ├── accounts/
│   │   ├── models.py           # Account data model
│   │   ├── store.py            # Token store abstraction
│   │   └── dependencies.py     # Shared token store instance
│   └── connectors/
│       ├── base.py             # Connector interface
│       └── gmail.py            # Gmail connector implementation
├── tests/
│   ├── test_auth.py
│   ├── test_health.py
│   ├── test_token_store.py
│   ├── test_account_linking.py
│   └── test_gmail_connector.py
├── requirements.txt
└── pyproject.toml
```

## Testing Strategy

**Automated tests cover:**
- JWT creation and validation
- Authorization header enforcement
- Token store read/write behavior
- Account linking logic
- Connector interfaces (mocked)

**Manual integration tests cover:**
- OAuth token generation flow
- Real Gmail API calls
- End-to-end `/sources/gmail/messages` flow

## Key Engineering Decisions

- **Pluggable connector system** — new providers are added by implementing a base interface, with zero changes to core logic
- **Single shared token store via dependency injection** — eliminates the multiple-instance bug that caused "account not linked" errors despite successful linking
- **Server-side token storage** — OAuth tokens never leave the backend, keeping client-facing auth limited to short-lived JWTs
- **Strict v1 scope** — features like automatic token refresh and background sync are intentionally deferred to keep the core architecture clean and auditable

## v1 Scope

**Included:**
- JWT-based authentication
- OAuth account linking
- Secure server-side token storage
- Gmail connector with real API integration
- Normalized provider response format
- Source-specific API endpoints

**Deferred to v2:**
- OAuth redirect & callback automation
- Automatic token refresh
- Background sync workers
- Additional connectors (Drive, Notion, Slack)

## Running Locally

```bash
pip install -r requirements.txt
uvicorn omnibridge.main:app --reload
# API: http://127.0.0.1:8000
# Docs: http://127.0.0.1:8000/docs
```
