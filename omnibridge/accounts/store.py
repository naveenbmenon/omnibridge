from typing import Dict, List, Optional
from omnibridge.accounts.models import Account


class InMemoryTokenStore:
    def __init__(self):
        # Structure:
        # { user_id: { provider: Account } }
        self._store: Dict[str, Dict[str, Account]] = {}

    def save_account(self, account: Account) -> None:
        if account.user_id not in self._store:
            self._store[account.user_id] = {}

        self._store[account.user_id][account.provider] = account

    def get_account(self, user_id: str, provider: str) -> Optional[Account]:
        return self._store.get(user_id, {}).get(provider)

    def list_accounts(self, user_id: str) -> List[Account]:
        return list(self._store.get(user_id, {}).values())
