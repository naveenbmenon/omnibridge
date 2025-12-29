from fastapi import APIRouter, Depends, HTTPException, status

from omnibridge.auth.dependencies import require_authentication
from omnibridge.accounts.dependencies import token_store  # ✅ SHARED STORE
from omnibridge.connectors.gmail import GmailConnector

router = APIRouter(prefix="/sources")

# Connector uses the SAME shared store
gmail_connector = GmailConnector(token_store=token_store)


@router.get("/gmail/messages")
def fetch_gmail_messages(
    payload: dict = Depends(require_authentication),
):
    user_id = payload["user_id"]

    try:
        results = gmail_connector.fetch(user_id=user_id)
        return results
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
