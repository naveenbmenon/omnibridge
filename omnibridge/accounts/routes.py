from fastapi import APIRouter, Depends
from datetime import datetime, timedelta, timezone

from omnibridge.auth.dependencies import require_authentication
from omnibridge.accounts.models import Account
from omnibridge.accounts.dependencies import token_store  # ✅ SHARED STORE

router = APIRouter(prefix="/accounts")


@router.post("/link")
def link_account(
    data: dict,
    payload: dict = Depends(require_authentication),
):
    user_id = payload["user_id"]

    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=data["expires_in"]
    )

    account = Account(
        user_id=user_id,
        provider=data["provider"],
        provider_account_id=data["provider_account_id"],
        access_token=data["access_token"],
        refresh_token=data.get("refresh_token"),
        expires_at=expires_at,
        scopes=data.get("scopes", []),
        created_at=datetime.now(timezone.utc),
    )

    token_store.save_account(account)

    return {"status": "linked"}


@router.get("")
def list_accounts(
    payload: dict = Depends(require_authentication),
):
    user_id = payload["user_id"]

    accounts = token_store.list_accounts(user_id)

    return [
        {
            "provider": account.provider,
            "provider_account_id": account.provider_account_id,
            "scopes": account.scopes,
            "expires_at": account.expires_at.isoformat(),
            "created_at": account.created_at.isoformat(),
        }
        for account in accounts
    ]


@router.get("/{provider}")
def get_account(
    provider: str,
    payload: dict = Depends(require_authentication),
):
    user_id = payload["user_id"]

    account = token_store.get_account(user_id, provider)

    if not account:
        return {"linked": False}

    return {
        "linked": True,
        "provider": account.provider,
        "provider_account_id": account.provider_account_id,
        "scopes": account.scopes,
        "expires_at": account.expires_at.isoformat(),
        "created_at": account.created_at.isoformat(),
    }
