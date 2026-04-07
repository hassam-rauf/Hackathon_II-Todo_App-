"""JWT verification middleware for FastAPI.

Task: T-037
Ref: specs/phase2-web/authentication/plan.md — Backend Middleware

Verifies EdDSA JWT tokens issued by Better Auth's JWT plugin.
Public keys are fetched from the JWKS endpoint at the frontend auth server.
"""

import os

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

security = HTTPBearer()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
JWKS_URL = f"{FRONTEND_URL}/api/auth/jwks"

_jwks_client = PyJWKClient(JWKS_URL, cache_keys=True, lifespan=3600)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Verify JWT and return user payload.

    Returns dict with 'sub' (user_id), 'email', 'name', etc.
    Raises 401 for missing, invalid, or expired tokens.
    """
    try:
        signing_key = _jwks_client.get_signing_key_from_jwt(credentials.credentials)
        payload = jwt.decode(
            credentials.credentials,
            signing_key.key,
            algorithms=["EdDSA"],
            audience=FRONTEND_URL,
            issuer=FRONTEND_URL,
        )
        if "sub" not in payload:
            raise HTTPException(status_code=401, detail="Invalid token: missing sub")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Auth error: {e}")
