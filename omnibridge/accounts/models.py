from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Account:
    user_id: str
    provider: str
    provider_account_id: str
    access_token: str
    refresh_token: Optional[str]
    expires_at: datetime
    scopes: List[str]
    created_at: datetime
