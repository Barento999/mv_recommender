from fastapi import APIRouter, HTTPException, status
from app.schemas.rating import RatingCreate, RatingResponse
from app.services.rating_service import (
    add_rating,
    get_user_ratings,
    get_rating,
)
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/ratings", tags=["ratings"])

@router.post("/add", response_model=dict)
async def add_user_rating(
    rating_data: RatingCreate,
    current_user: User = Depends(get_current_user),
):
    try:
        rating = await add_rating(
            str(current_user._id),
            rating_data.movie_id,
            rating_data.rating,
        )
        return {
            "message": "Rating saved",
            "rating": {
                "_id": str(rating._id),
                "user_id": str(rating.user_id),
                "movie_id": str(rating.movie_id),
                "rating": rating.rating,
                "created_at": rating.created_at,
            },
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("")
async def get_user_ratings_list(
    current_user: User = Depends(get_current_user),
):
    ratings = await get_user_ratings(str(current_user._id))
    return {
        "ratings": [
            {
                "_id": str(r._id),
                "user_id": str(r.user_id),
                "movie_id": str(r.movie_id),
                "rating": r.rating,
                "created_at": r.created_at,
            }
            for r in ratings
        ]
    }

@router.get("/{movie_id}", response_model=dict)
async def get_movie_rating(
    movie_id: str,
    current_user: User = Depends(get_current_user),
):
    rating = await get_rating(str(current_user._id), movie_id)
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")

    return {
        "_id": str(rating._id),
        "user_id": str(rating.user_id),
        "movie_id": str(rating.movie_id),
        "rating": rating.rating,
        "created_at": rating.created_at,
    }
