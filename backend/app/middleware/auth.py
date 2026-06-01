from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.utils.security import decode_token
from app.services.user_service import get_user_by_id

from typing import Optional

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    return user

async def get_current_user_optional(
    credentials: Optional[HTTPAuthCredentials] = Depends(security),
) -> Optional[dict]:
    if not credentials:
        return None

    try:
        token = credentials.credentials
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        user = await get_user_by_id(user_id)
        return user
    except Exception:
        return None
