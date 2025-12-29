
# OmniBridge v1

**A Pluggable API Gateway for Secure OAuth-Based Access to Third-Party Services**

---

## 🚀 Overview

**OmniBridge** is a backend platform that acts as a **secure, unified gateway** between applications and third-party services such as Gmail.

Instead of every application individually handling OAuth, tokens, rate limits, and provider-specific APIs, OmniBridge centralizes this complexity behind a **clean, normalized API**.

OmniBridge v1 focuses on **correct architecture, security, and real-world integration**, rather than UI or automation polish.

---

## 🎯 Goals of OmniBridge v1

* Centralize OAuth integrations
* Securely store and manage provider tokens
* Expose a unified API for external services
* Normalize provider-specific data
* Serve as a backend platform for future applications (e.g., Unified Search)

---

## 🧠 Core Concepts

### Why OmniBridge?

Every third-party service has:

* Different OAuth flows
* Different APIs
* Different response formats

OmniBridge abstracts this complexity into a **single platform**, allowing applications to interact with multiple services using a consistent interface.

---

## 🏗️ High-Level Architecture

```
Client / App (Postman, Future UI)
        ↓
JWT Authentication (OmniBridge)
        ↓
OmniBridge API Layer
        ↓
Connector Layer (Gmail)
        ↓
External Provider APIs
```

Key principle:

> **Applications never talk directly to third-party APIs. OmniBridge does.**

---

## 🔐 Authentication & Authorization

### JWT (OmniBridge Authentication)

* OmniBridge issues JWTs to identify users
* JWTs are required for all protected endpoints
* JWTs are stateless and validated on every request

### OAuth (Provider Authorization)

* OAuth access & refresh tokens are obtained from providers (e.g., Google)
* Tokens are **stored securely server-side**
* Tokens are never exposed to clients

---

## 🔑 Token Types Used

| Token               | Purpose                           |
| ------------------- | --------------------------------- |
| JWT                 | Identifies user within OmniBridge |
| OAuth Access Token  | Calls provider APIs               |
| OAuth Refresh Token | Renews expired access tokens      |

---

## 🧩 Connector Architecture

OmniBridge uses a **pluggable connector system**.

Each connector:

* Knows how to talk to one provider
* Converts provider responses into a normalized format
* Is isolated from OmniBridge core logic

### Example: Gmail Connector

Responsibilities:

* Authenticate with Gmail API
* Fetch recent emails
* Normalize Gmail responses

Normalized email structure:

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

---

## 📁 Project Structure

```
omnibridge_v1/
├── omnibridge/
│   ├── main.py                 # FastAPI app entry point
│   │
│   ├── api/
│   │   ├── auth_routes.py      # JWT issuing endpoints
│   │   ├── accounts.py         # Account linking & listing
│   │   ├── sources.py          # Provider data access endpoints
│   │
│   ├── auth/
│   │   ├── jwt.py              # JWT creation & verification
│   │   └── dependencies.py     # Auth dependency injection
│   │
│   ├── accounts/
│   │   ├── models.py           # Account data model
│   │   ├── store.py            # Token store abstraction
│   │   └── dependencies.py     # Shared token store instance
│   │
│   ├── connectors/
│   │   ├── base.py             # Connector interface
│   │   └── gmail.py            # Gmail connector implementation
│
├── tests/
│   ├── test_auth.py
│   ├── test_health.py
│   ├── test_token_store.py
│   ├── test_account_linking.py
│   └── test_gmail_connector.py
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 🧪 Testing Strategy

### Automated Tests

* JWT validation
* Authorization header enforcement
* Token store behavior
* Account linking logic
* Connector interfaces (mocked)

### Manual Integration Tests

* OAuth token generation
* Real Gmail API calls
* End-to-end `/sources/gmail/messages` flow

This hybrid approach ensures:

* Fast feedback during development
* Confidence in real-world behavior

---

## ⚠️ Key Challenges Encountered (and Solutions)

### 1. Gmail API returning empty results

**Cause:** Gmail UI search ≠ Gmail API search
**Solution:** Fetch recent messages in v1 for reliability

---

### 2. Connector code not executing

**Cause:** Incorrect endpoint path used during testing
**Solution:** Isolated `/sources/gmail/messages` endpoint and tested directly

---

### 3. “Google account not linked” despite successful linking

**Cause:** Multiple in-memory token store instances
**Solution:** Introduced a **single shared token store** via dependency injection

---

### 4. “Invalid token” errors after restart

**Cause:** JWTs invalidated on server restart
**Solution:** Re-issued JWTs and clarified token lifecycle

---

## ✅ Scope of OmniBridge v1

### Included

* JWT-based authentication
* OAuth account linking
* Secure token storage
* Gmail connector with real API integration
* Normalized provider data
* Source-specific API endpoints

### Explicitly Excluded

* OAuth redirect automation
* Automatic token refresh
* Background sync jobs
* Full-text search indexing
* Multi-provider aggregation

These are deferred to v2.

---

## 🔮 Planned Future Work (v2+)

* OAuth redirect & callback flow
* Automatic token refresh
* Provider pagination & indexing
* Background sync workers
* Additional connectors (Drive, Notion, Slack)
* Unified `/search` aggregation endpoint

---

## 🧩 Integration with Other Projects

OmniBridge is designed to act as a **platform service**.

Example usage:

* Unified Search backend consumes OmniBridge APIs
* Future apps reuse the same OAuth integrations
* No duplication of provider logic

---

## 🏁 Project Status

**OmniBridge v1 is complete and stable.**

The project is intentionally paused at this stage to:

* Preserve architectural clarity
* Avoid over-polishing
* Allow focus on additional portfolio projects

Further development will resume as OmniBridge v2.

---

## 📌 Key Takeaway

> OmniBridge v1 demonstrates real-world backend engineering: secure auth, OAuth integration, connector-based architecture, and production-style problem solving.

---

