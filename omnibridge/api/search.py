from fastapi import APIRouter, Depends, HTTPException, status, Query

from omnibridge.auth.dependencies import require_authentication
from omnibridge.accounts.store import InMemoryTokenStore
from omnibridge.connectors.gmail import GmailConnector

router = APIRouter()

# Shared store (Phase 3 v1)
token_store = InMemoryTokenStore()

# Available connectors (extendable)
gmail_connector = GmailConnector(token_store=token_store)

CONNECTORS = {
    "gmail": gmail_connector,
    # "drive": drive_connector,  # future
}


@router.get("/search")
def unified_search(
    q: str = Query(..., description="Search query"),
    sources: str | None = Query(
        default=None,
        description="Comma-separated list of sources (e.g., gmail,drive)",
    ),
    payload: dict = Depends(require_authentication),
):
    user_id = payload["user_id"]

    # Decide which connectors to use
    if sources:
        requested = {s.strip() for s in sources.split(",")}
        connectors = [
            CONNECTORS[name]
            for name in requested
            if name in CONNECTORS
        ]
    else:
        connectors = list(CONNECTORS.values())

    results: list[dict] = []

    for connector in connectors:
        try:
            data = connector.fetch(user_id=user_id, query=q)
            results.extend(data)
        except Exception:
            # If a connector fails (e.g., not linked),
            # we skip it instead of failing the whole search
            continue

    return results
