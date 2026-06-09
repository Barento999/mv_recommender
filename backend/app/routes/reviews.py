from fastapi import Depends, APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from app.services.review_service import (
    create_review,
    get_movie_reviews,
    get_user_review,
    delete_review,
    mark_helpful,
    get_movie_review_stats,
    get_user_reviews,
)
from app.middleware.auth import get_current_user
from app.models.user import User
from typing import Optional

router = APIRouter(prefix="/reviews", tags=["reviews"])

class ReviewCreate(BaseModel):
    rating: int
    title: str
    content: str

@router.post("/movie/{movie_id}")
async def create_movie_review(
    movie_id: str,
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
):
    """Create or update a review for a movie."""
    if not (1 <= review_data.rating <= 10):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 10"
        )
    
    if len(review_data.title) < 3 or len(review_data.title) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title must be between 3 and 100 characters"
        )
    
    if len(review_data.content) < 10 or len(review_data.content) > 5000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content must be between 10 and 5000 characters"
        )
    
    try:
        review = await create_review(
            str(current_user._id),
            movie_id,
            review_data.rating,
            review_data.title,
            review_data.content
        )
        return {
            "message": "Review created/updated successfully",
            "review": {
                "review_id": str(review._id),
                "rating": review.rating,
                "title": review.title,
                "content": review.content,
                "created_at": review.created_at,
                "updated_at": review.updated_at,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/movie/{movie_id}")
async def get_reviews(
    movie_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("helpful", pattern="^(recent|helpful|rating_high|rating_low)$"),
):
    """Get reviews for a movie."""
    reviews, total = await get_movie_reviews(movie_id, skip, limit, sort_by)
    return {
        "reviews": reviews,
        "total": total,
        "skip": skip,
        "limit": limit,
        "sort_by": sort_by,
    }

@router.get("/movie/{movie_id}/stats")
async def get_review_stats(movie_id: str):
    """Get review statistics for a movie."""
    stats = await get_movie_review_stats(movie_id)
    return {
        "stats": stats,
        "message": "Review statistics",
    }

@router.get("/movie/{movie_id}/user-review")
async def get_user_movie_review(
    movie_id: str,
    current_user: User = Depends(get_current_user),
):
    """Get current user's review for a movie."""
    review = await get_user_review(str(current_user._id), movie_id)
    return {
        "review": review,
        "has_review": review is not None,
    }

@router.delete("/movie/{movie_id}")
async def delete_movie_review(
    movie_id: str,
    current_user: User = Depends(get_current_user),
):
    """Delete a review."""
    success = await delete_review(str(current_user._id), movie_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return {"message": "Review deleted successfully"}

@router.post("/{review_id}/helpful")
async def mark_review_helpful(
    review_id: str,
    current_user: User = Depends(get_current_user),
):
    """Mark a review as helpful."""
    success = await mark_helpful(review_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return {"message": "Review marked as helpful"}

@router.get("/user/my-reviews")
async def get_my_reviews(
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
):
    """Get current user's reviews."""
    reviews = await get_user_reviews(str(current_user._id), limit)
    return {
        "reviews": reviews,
        "count": len(reviews),
    }
