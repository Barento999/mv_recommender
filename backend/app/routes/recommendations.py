from fastapi import APIRouter, Query
from app.services.recommendation_service import (
    get_recommendations,
    get_similar_movies,
)
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("")
async def get_user_recommendations(
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
):
    recommendations = await get_recommendations(str(current_user._id), limit)
    return {
        "recommendations": [
            {
                "_id": str(m._id),
                "title": m.title,
                "genre": m.genre,
                "year": m.year,
                "rating": m.rating,
                "description": m.description,
                "poster_url": m.poster_url,
                "trailer_url": m.trailer_url,
                "created_at": m.created_at,
            }
            for m in recommendations
        ],
        "count": len(recommendations),
        "message": "Recommendations based on your favorites",
    }

@router.get("/similar/{movie_id}")
async def get_similar(
    movie_id: str,
    limit: int = Query(5, ge=1, le=100),
):
    similar = await get_similar_movies(movie_id, limit)
    return {
        "similar": [
            {
                "_id": str(m._id),
                "title": m.title,
                "genre": m.genre,
                "year": m.year,
                "rating": m.rating,
                "description": m.description,
                "poster_url": m.poster_url,
                "trailer_url": m.trailer_url,
                "created_at": m.created_at,
            }
            for m in similar
        ],
        "count": len(similar),
    }
