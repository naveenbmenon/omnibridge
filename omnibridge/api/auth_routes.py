from fastapi import APIRouter
from datetime import datetime, timedelta
from jose import jwt

from omnibridge.auth.config import JWT_SECRET_KEY, JWT_ALGORITHM

router = APIRouter(prefix="/auth")


@router.post("/token")
def issue_token(email: str):
    # Phase 1: simple deterministic identity
    user_id = email  # later this maps to a real user record

    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer",
    }
