from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from app.schemas.user import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services.user_service import create_user, authenticate_user
from app.utils.security import create_access_token
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserRegister):
    try:
        user = await create_user(user_data.name, user_data.email, user_data.password)
        access_token = create_access_token(data={"sub": str(user._id)})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "_id": str(user._id),
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at,
            },
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(data={"sub": str(user._id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "_id": str(user._id),
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
        },
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "_id": str(current_user._id),
        "name": current_user.name,
        "email": current_user.email,
        "created_at": current_user.created_at,
    }
