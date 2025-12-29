from jose import jwt, JWTError
from omnibridge.auth.config import JWT_SECRET_KEY, JWT_ALGORITHM


def verify_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        raise ValueError("Invalid JWT")
