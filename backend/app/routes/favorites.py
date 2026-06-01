from fastapi import Depends, APIRouter, HTTPException, status, Query
from app.services.favorite_service import (
    add_favorite,
    remove_favorite,
    get_user_favorites,
    is_favorite,
)
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/favorites", tags=["favorites"])

@router.post("/add/{movie_id}")
async def add_favorite_movie(
    movie_id: str,
    current_user: User = Depends(get_current_user),
):
    try:
        favorite = await add_favorite(str(current_user._id), movie_id)
        return {
            "message": "Added to favorites",
            "favorite": {
                "_id": str(favorite._id),
                "user_id": str(favorite.user_id),
                "movie_id": str(favorite.movie_id),
                "created_at": favorite.created_at,
            },
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/remove/{movie_id}")
async def remove_favorite_movie(
    movie_id: str,
    current_user: User = Depends(get_current_user),
):
    success = await remove_favorite(str(current_user._id), movie_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")

    return {"message": "Removed from favorites"}

@router.get("")
async def get_favorites(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
):
    favorites, total = await get_user_favorites(str(current_user._id), skip, limit)
    return {
        "favorites": favorites,
        "total": total,
        "skip": skip,
        "limit": limit,
    }

@router.get("/check/{movie_id}")
async def check_favorite(
    movie_id: str,
    current_user: User = Depends(get_current_user),
):
    is_fav = await is_favorite(str(current_user._id), movie_id)
    return {"is_favorite": is_fav}
