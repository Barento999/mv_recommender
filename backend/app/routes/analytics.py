from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_database
from app.middleware.auth import get_current_user
from app.middleware.rbac import require_role_or_higher
from app.models.user import User
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview")
async def get_analytics_overview(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: User = Depends(require_role_or_higher("moderator")),
):
    """Get overall system analytics."""
    try:
        # Get collections
        users_collection = db["users"]
        movies_collection = db["movies"]
        ratings_collection = db["ratings"]
        favorites_collection = db["favorites"]

        # Count totals
        total_users = await users_collection.count_documents({})
        total_movies = await movies_collection.count_documents({})
        total_ratings = await ratings_collection.count_documents({})
        total_favorites = await favorites_collection.count_documents({})

        # Calculate averages
        ratings_data = await ratings_collection.aggregate([
            {
                "$group": {
                    "_id": None,
                    "avg_rating": {"$avg": "$rating"},
                    "min_rating": {"$min": "$rating"},
                    "max_rating": {"$max": "$rating"},
                }
            }
        ]).to_list(None)

        rating_stats = ratings_data[0] if ratings_data else {
            "avg_rating": 0,
            "min_rating": 0,
            "max_rating": 0
        }

        # Active users (rated or favorited in last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        active_users = await ratings_collection.distinct(
            "user_id",
            {"created_at": {"$gte": seven_days_ago}}
        )

        return {
            "total_users": total_users,
            "total_movies": total_movies,
            "total_ratings": total_ratings,
            "total_favorites": total_favorites,
            "avg_rating": round(rating_stats.get("avg_rating", 0), 2),
            "min_rating": rating_stats.get("min_rating", 0),
            "max_rating": rating_stats.get("max_rating", 0),
            "active_users_7d": len(active_users),
            "engagement_rate": round((len(active_users) / max(total_users, 1)) * 100, 2)
        }

    except Exception as e:
        logger.error(f"Error fetching analytics overview: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch analytics overview")


@router.get("/ratings-distribution")
async def get_ratings_distribution(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: User = Depends(require_role_or_higher("moderator")),
):
    """Get distribution of ratings (1-10)."""
    try:
        ratings_collection = db["ratings"]
        
        # Group ratings by value
        distribution = await ratings_collection.aggregate([
            {
                "$group": {
                    "_id": "$rating",
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"_id": 1}}
        ]).to_list(None)

        # Fill missing ratings with 0
        full_distribution = {}
        for i in range(1, 11):
            full_distribution[i] = 0

        for item in distribution:
            full_distribution[int(item["_id"])] = item["count"]

        return {
            "distribution": [
                {"rating": rating, "count": count}
                for rating, count in sorted(full_distribution.items())
            ]
        }

    except Exception as e:
        logger.error(f"Error fetching ratings distribution: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch ratings distribution")


@router.get("/genre-analytics")
async def get_genre_analytics(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: User = Depends(require_role_or_higher("moderator")),
):
    """Get analytics by genre."""
    try:
        movies_collection = db["movies"]
        ratings_collection = db["ratings"]

        # Get genre counts
        genre_data = await movies_collection.aggregate([
            {
                "$unwind": "$genre"
            },
            {
                "$group": {
                    "_id": "$genre",
                    "movie_count": {"$sum": 1},
                    "avg_rating": {"$avg": "$rating"}
                }
            },
            {"$sort": {"movie_count": -1}},
            {"$limit": 15}
        ]).to_list(None)

        # Get rating counts per genre
        genres_with_ratings = []
        for item in genre_data:
            genre = item["_id"]
            # Count ratings for this genre
            rating_count = await ratings_collection.count_documents({
                "genre": genre
            })
            
            genres_with_ratings.append({
                "genre": genre,
                "movie_count": item["movie_count"],
                "avg_rating": round(item["avg_rating"], 2),
                "total_ratings": rating_count
            })

        return {"genres": genres_with_ratings}

    except Exception as e:
        logger.error(f"Error fetching genre analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch genre analytics")


@router.get("/user-engagement")
async def get_user_engagement(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: User = Depends(require_role_or_higher("moderator")),
):
    """Get user engagement metrics (optimized)."""
    try:
        users_collection = db["users"]
        ratings_collection = db["ratings"]
        favorites_collection = db["favorites"]

        total_users = await users_collection.count_documents({})
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        # Get active users in 30 days via aggregation
        active_users_30d_list = await ratings_collection.distinct(
            "user_id",
            {"created_at": {"$gte": thirty_days_ago}}
        )
        active_users_30d = len(active_users_30d_list)

        # Get super users (20+ ratings or 10+ favorites) - using aggregation
        super_users_ratings = await ratings_collection.aggregate([
            {
                "$group": {
                    "_id": "$user_id",
                    "rating_count": {"$sum": 1}
                }
            },
            {
                "$match": {"rating_count": {"$gte": 20}}
            }
        ]).to_list(None)

        super_user_ids = set(u["_id"] for u in super_users_ratings)

        super_users_favorites = await favorites_collection.aggregate([
            {
                "$group": {
                    "_id": "$user_id",
                    "favorite_count": {"$sum": 1}
                }
            },
            {
                "$match": {"favorite_count": {"$gte": 10}}
            }
        ]).to_list(None)

        super_user_ids.update(u["_id"] for u in super_users_favorites)
        super_users = len(super_user_ids)

        # Dormant users = total - active in 30 days (simplified estimate)
        dormant_users = max(0, total_users - active_users_30d)

        return {
            "total_users": total_users,
            "active_users_30d": active_users_30d,
            "super_users": super_users,
            "dormant_users": dormant_users,
            "engagement_categories": {
                "active": active_users_30d,
                "super": super_users,
                "dormant": dormant_users,
                "regular": max(0, total_users - super_users - dormant_users)
            }
        }

    except Exception as e:
        logger.error(f"Error fetching user engagement: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch user engagement")


@router.get("/top-movies-analytics")
async def get_top_movies_analytics(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: User = Depends(require_role_or_higher("moderator")),
):
    """Get top movies by various metrics."""
    try:
        movies_collection = db["movies"]
        ratings_collection = db["ratings"]
        favorites_collection = db["favorites"]

        # Top rated movies
        top_rated = await movies_collection.find({}).sort("rating", -1).limit(10).to_list(None)

        # Most favorited
        most_favorited = await favorites_collection.aggregate([
            {
                "$group": {
                    "_id": "$movie_id",
                    "favorite_count": {"$sum": 1}
                }
            },
            {"$sort": {"favorite_count": -1}},
            {"$limit": 10}
        ]).to_list(None)

        # Get movie details for most favorited
        favorited_movies = []
        for item in most_favorited:
            movie = await movies_collection.find_one({"_id": item["_id"]})
            if movie:
                favorited_movies.append({
                    "title": movie.get("title", "Unknown"),
                    "rating": movie.get("rating", 0),
                    "favorite_count": item["favorite_count"],
                    "year": movie.get("year", 0)
                })

        # Most rated (by number of ratings)
        most_rated = await ratings_collection.aggregate([
            {
                "$group": {
                    "_id": "$movie_id",
                    "rating_count": {"$sum": 1},
                    "avg_rating": {"$avg": "$rating"}
                }
            },
            {"$sort": {"rating_count": -1}},
            {"$limit": 10}
        ]).to_list(None)

        rated_movies = []
        for item in most_rated:
            movie = await movies_collection.find_one({"_id": item["_id"]})
            if movie:
                rated_movies.append({
                    "title": movie.get("title", "Unknown"),
                    "rating_count": item["rating_count"],
                    "avg_rating": round(item["avg_rating"], 2),
                    "year": movie.get("year", 0)
                })

        return {
            "top_rated": [
                {
                    "title": m.get("title", "Unknown"),
                    "rating": m.get("rating", 0),
                    "year": m.get("year", 0)
                }
                for m in top_rated
            ],
            "most_favorited": favorited_movies,
            "most_rated": rated_movies
        }

    except Exception as e:
        logger.error(f"Error fetching top movies analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch top movies analytics")


@router.get("/timeline-stats")
async def get_timeline_stats(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: User = Depends(require_role_or_higher("moderator")),
):
    """Get ratings timeline for last 30 days."""
    try:
        ratings_collection = db["ratings"]
        
        # Get ratings for last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        daily_stats = await ratings_collection.aggregate([
            {
                "$match": {
                    "created_at": {"$gte": thirty_days_ago}
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}
                    },
                    "count": {"$sum": 1},
                    "avg_rating": {"$avg": "$rating"}
                }
            },
            {"$sort": {"_id": 1}}
        ]).to_list(None)

        return {
            "timeline": [
                {
                    "date": item["_id"],
                    "ratings_count": item["count"],
                    "avg_rating": round(item["avg_rating"], 2)
                }
                for item in daily_stats
            ]
        }

    except Exception as e:
        logger.error(f"Error fetching timeline stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch timeline stats")
