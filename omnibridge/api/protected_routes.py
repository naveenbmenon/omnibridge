from fastapi import APIRouter, Depends
from omnibridge.auth.dependencies import require_authentication

router = APIRouter()


@router.get("/protected")
def protected_endpoint(payload: dict = Depends(require_authentication)):
    return {
        "user_id": payload["user_id"]
    }
