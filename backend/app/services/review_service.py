from app.database import get_database
from app.models.review import Review
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

async def create_review(
    user_id: str, 
    movie_id: str, 
    rating: int,
    title: str,
    content: str
) -> Review:
    """Create a new review for a movie."""
    db = get_database()
    
    # Check if user already reviewed this movie
    existing = await db.reviews.find_one({
        "user_id": ObjectId(user_id),
        "movie_id": ObjectId(movie_id)
    })
    
    if existing:
        # Update existing review
        result = await db.reviews.find_one_and_update(
            {"_id": existing["_id"]},
            {
                "$set": {
                    "rating": rating,
                    "title": title,
                    "content": content,
                    "updated_at": datetime.utcnow()
                }
            },
            return_document=True,
        )
        return Review.from_dict(result)
    
    # Create new review
    review = Review(
        user_id=ObjectId(user_id),
        movie_id=ObjectId(movie_id),
        rating=rating,
        title=title,
        content=content
    )
    result = await db.reviews.insert_one(review.to_dict())
    review._id = result.inserted_id
    return review

async def get_movie_reviews(
    movie_id: str,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "helpful"
) -> tuple[List[dict], int]:
    """Get reviews for a movie."""
    db = get_database()
    query = {"movie_id": ObjectId(movie_id)}
    
    # Sort options
    sort_map = {
        "recent": [("created_at", -1)],
        "helpful": [("helpful_count", -1)],
        "rating_high": [("rating", -1)],
        "rating_low": [("rating", 1)],
    }
    sort_option = sort_map.get(sort_by, [("helpful_count", -1)])
    
    reviews_data = await db.reviews.find(query).sort(*sort_option).skip(skip).limit(limit).to_list(None)
    total = await db.reviews.count_documents(query)

    reviews = []
    for review in reviews_data:
        # Get user info
        user = await db.users.find_one({"_id": review["user_id"]})
        review_dict = {
            "review_id": str(review["_id"]),
            "user_id": str(review["user_id"]),
            "user_name": user.get("name", "Anonymous") if user else "Anonymous",
            "movie_id": str(review["movie_id"]),
            "rating": review.get("rating"),
            "title": review.get("title"),
            "content": review.get("content"),
            "helpful_count": review.get("helpful_count", 0),
            "created_at": review.get("created_at"),
            "updated_at": review.get("updated_at"),
        }
        reviews.append(review_dict)

    return reviews, total

async def get_user_review(user_id: str, movie_id: str) -> Optional[dict]:
    """Get user's review for a specific movie."""
    db = get_database()
    
    review = await db.reviews.find_one({
        "user_id": ObjectId(user_id),
        "movie_id": ObjectId(movie_id)
    })
    
    if not review:
        return None
    
    user = await db.users.find_one({"_id": review["user_id"]})
    return {
        "review_id": str(review["_id"]),
        "user_id": str(review["user_id"]),
        "user_name": user.get("name", "Anonymous") if user else "Anonymous",
        "movie_id": str(review["movie_id"]),
        "rating": review.get("rating"),
        "title": review.get("title"),
        "content": review.get("content"),
        "helpful_count": review.get("helpful_count", 0),
        "created_at": review.get("created_at"),
        "updated_at": review.get("updated_at"),
    }

async def delete_review(user_id: str, movie_id: str) -> bool:
    """Delete a review."""
    db = get_database()
    try:
        result = await db.reviews.delete_one({
            "user_id": ObjectId(user_id),
            "movie_id": ObjectId(movie_id)
        })
        return result.deleted_count > 0
    except Exception:
        return False

async def mark_helpful(review_id: str) -> bool:
    """Mark a review as helpful."""
    db = get_database()
    try:
        result = await db.reviews.find_one_and_update(
            {"_id": ObjectId(review_id)},
            {"$inc": {"helpful_count": 1}},
            return_document=True
        )
        return result is not None
    except Exception:
        return False

async def get_movie_review_stats(movie_id: str) -> dict:
    """Get review statistics for a movie."""
    db = get_database()
    query = {"movie_id": ObjectId(movie_id)}
    
    all_reviews = await db.reviews.find(query).to_list(None)
    
    if not all_reviews:
        return {
            "total_reviews": 0,
            "average_rating": 0,
            "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
        }
    
    # Calculate statistics
    total = len(all_reviews)
    avg_rating = sum(r.get("rating", 0) for r in all_reviews) / total if total > 0 else 0
    
    # Rating distribution
    rating_dist = {i: 0 for i in range(1, 11)}
    for review in all_reviews:
        rating = review.get("rating", 0)
        if 1 <= rating <= 10:
            rating_dist[rating] += 1
    
    return {
        "total_reviews": total,
        "average_rating": round(avg_rating, 2),
        "rating_distribution": rating_dist
    }

async def get_user_reviews(user_id: str, limit: int = 10) -> List[dict]:
    """Get all reviews by a user."""
    db = get_database()
    
    reviews_data = await db.reviews.find({"user_id": ObjectId(user_id)}).sort("created_at", -1).limit(limit).to_list(None)
    
    reviews = []
    for review in reviews_data:
        # Get movie info
        movie = await db.movies.find_one({"_id": review["movie_id"]})
        review_dict = {
            "review_id": str(review["_id"]),
            "user_id": str(review["user_id"]),
            "movie_id": str(review["movie_id"]),
            "movie_title": movie.get("title", "Unknown") if movie else "Unknown",
            "rating": review.get("rating"),
            "title": review.get("title"),
            "content": review.get("content"),
            "helpful_count": review.get("helpful_count", 0),
            "created_at": review.get("created_at"),
            "updated_at": review.get("updated_at"),
        }
        reviews.append(review_dict)

    return reviews
