from datetime import datetime, timedelta, timezone

from omnibridge.accounts.models import Account
from omnibridge.accounts.store import InMemoryTokenStore


def make_account(
    user_id="user@example.com",
    provider="google",
    provider_account_id="user@gmail.com",
):
    return Account(
        user_id=user_id,
        provider=provider,
        provider_account_id=provider_account_id,
        access_token="access-token",
        refresh_token="refresh-token",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        scopes=["scope.read"],
        created_at=datetime.now(timezone.utc),
    )


def test_store_and_get_account():
    store = InMemoryTokenStore()
    account = make_account()

    store.save_account(account)

    fetched = store.get_account("user@example.com", "google")

    assert fetched is not None
    assert fetched.user_id == "user@example.com"
    assert fetched.provider == "google"
    assert fetched.provider_account_id == "user@gmail.com"

def test_get_account_returns_none_if_not_found():
    store = InMemoryTokenStore()

    result = store.get_account("user@example.com", "google")

    assert result is None


def test_users_are_isolated():
    store = InMemoryTokenStore()

    alice_account = make_account(user_id="alice@example.com")
    bob_account = make_account(
        user_id="bob@example.com",
        provider_account_id="bob@gmail.com",
    )

    store.save_account(alice_account)
    store.save_account(bob_account)

    alice_google = store.get_account("alice@example.com", "google")
    bob_google = store.get_account("bob@example.com", "google")

    assert alice_google.provider_account_id == "user@gmail.com"
    assert bob_google.provider_account_id == "bob@gmail.com"



def test_same_user_multiple_providers():
    store = InMemoryTokenStore()

    google_account = make_account(provider="google")
    notion_account = make_account(
        provider="notion",
        provider_account_id="notion-user-id",
    )

    store.save_account(google_account)
    store.save_account(notion_account)

    google = store.get_account("user@example.com", "google")
    notion = store.get_account("user@example.com", "notion")

    assert google is not None
    assert notion is not None
    assert google.provider == "google"
    assert notion.provider == "notion"



def test_list_accounts_for_user():
    store = InMemoryTokenStore()

    store.save_account(make_account(provider="google"))
    store.save_account(make_account(provider="notion"))

    accounts = store.list_accounts("user@example.com")

    providers = {a.provider for a in accounts}

    assert providers == {"google", "notion"}


