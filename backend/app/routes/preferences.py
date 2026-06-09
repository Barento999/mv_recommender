from fastapi import Depends, APIRouter, HTTPException
from app.database import get_database
from app.middleware.auth import get_current_user
from app.models.user import User
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/preferences", tags=["preferences"])


@router.get("")
async def get_user_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get user's preference settings."""
    try:
        user_obj_id = ObjectId(str(current_user._id)) if isinstance(current_user._id, str) else current_user._id
        
        # Get or create user preferences document
        preferences = await db.preferences.find_one({"user_id": user_obj_id})
        
        if not preferences:
            # Return default preferences
            return {
                "user_id": str(user_obj_id),
                "favorite_genres": [],
                "disliked_genres": [],
                "min_rating": 5.0,
                "max_year": 2026,
                "min_year": 1900,
                "language": "en",
                "notifications_enabled": True,
                "recommendations_frequency": "weekly"
            }
        
        return {
            "user_id": str(preferences.get("user_id", user_obj_id)),
            "favorite_genres": preferences.get("favorite_genres", []),
            "disliked_genres": preferences.get("disliked_genres", []),
            "min_rating": preferences.get("min_rating", 5.0),
            "max_year": preferences.get("max_year", 2026),
            "min_year": preferences.get("min_year", 1900),
            "language": preferences.get("language", "en"),
            "notifications_enabled": preferences.get("notifications_enabled", True),
            "recommendations_frequency": preferences.get("recommendations_frequency", "weekly")
        }
        
    except Exception as e:
        logger.error(f"Error getting preferences: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get preferences")


@router.put("")
async def update_user_preferences(
    preferences_data: Dict,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Update user's preference settings."""
    try:
        user_obj_id = ObjectId(str(current_user._id)) if isinstance(current_user._id, str) else current_user._id
        
        # Validate preferences data
        update_data = {
            "user_id": user_obj_id,
            "favorite_genres": preferences_data.get("favorite_genres", []),
            "disliked_genres": preferences_data.get("disliked_genres", []),
            "min_rating": max(0, min(10, float(preferences_data.get("min_rating", 5.0)))),
            "max_year": int(preferences_data.get("max_year", 2026)),
            "min_year": int(preferences_data.get("min_year", 1900)),
            "language": preferences_data.get("language", "en"),
            "notifications_enabled": bool(preferences_data.get("notifications_enabled", True)),
            "recommendations_frequency": preferences_data.get("recommendations_frequency", "weekly")
        }
        
        # Update preferences
        result = await db.preferences.update_one(
            {"user_id": user_obj_id},
            {"$set": update_data},
            upsert=True
        )
        
        logger.info(f"Updated preferences for user {user_obj_id}")
        
        return {
            "success": True,
            "message": "Preferences updated successfully",
            "preferences": update_data
        }
        
    except Exception as e:
        logger.error(f"Error updating preferences: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update preferences")


@router.get("/genres/available")
async def get_available_genres(
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get all available genres from movies collection."""
    try:
        # Get unique genres from all movies
        genres = await db.movies.distinct("genre")
        
        # Sort genres alphabetically
        genres = sorted(genres)
        
        return {
            "genres": genres,
            "count": len(genres)
        }
        
    except Exception as e:
        logger.error(f"Error getting genres: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get genres")


@router.get("/analysis")
async def get_preference_analysis(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get detailed analysis of user's preferences based on their activity."""
    try:
        user_obj_id = ObjectId(str(current_user._id)) if isinstance(current_user._id, str) else current_user._id
        
        # Get user's ratings
        user_ratings = await db.ratings.find({"user_id": user_obj_id}).to_list(None)
        
        if not user_ratings:
            return {
                "genre_preferences": {},
                "year_preferences": {},
                "rating_distribution": {},
                "top_genres": [],
                "average_rating": 0,
                "total_ratings": 0
            }
        
        # Get movie details for rated movies - handle both ObjectId and string formats
        movie_ids = []
        for r in user_ratings:
            movie_id = r.get("movie_id")
            if isinstance(movie_id, str):
                try:
                    if len(movie_id) == 24:  # Valid hex string
                        movie_ids.append(ObjectId(movie_id))
                    else:
                        movie_ids.append(movie_id)
                except Exception:
                    movie_ids.append(movie_id)
            else:
                movie_ids.append(movie_id)
        
        if not movie_ids:
            return {
                "genre_preferences": {},
                "year_preferences": {},
                "rating_distribution": {},
                "top_genres": [],
                "average_rating": 0,
                "total_ratings": 0
            }
        
        movies = await db.movies.find({"_id": {"$in": movie_ids}}).to_list(None)
        movies_map = {str(m["_id"]): m for m in movies}
        
        # Analyze preferences
        genre_preferences = {}
        year_preferences = {}
        rating_distribution = {}
        
        total_rating = 0
        
        for rating in user_ratings:
            try:
                user_rating = float(rating.get("rating", 0))
                movie_id = str(rating.get("movie_id", ""))
                
                total_rating += user_rating
                
                # Rating distribution
                rating_key = int(user_rating)
                rating_distribution[rating_key] = rating_distribution.get(rating_key, 0) + 1
                
                # Get movie details
                if movie_id in movies_map:
                    movie = movies_map[movie_id]
                    
                    # Genre preferences
                    for genre in movie.get("genre", []):
                        if genre not in genre_preferences:
                            genre_preferences[genre] = {"count": 0, "avg_rating": 0, "total": 0}
                        genre_preferences[genre]["count"] += 1
                        genre_preferences[genre]["total"] += user_rating
                        genre_preferences[genre]["avg_rating"] = genre_preferences[genre]["total"] / genre_preferences[genre]["count"]
                    
                    # Year preferences
                    year = movie.get("year", 0)
                    if year:
                        year_range = f"{int(year/10)*10}s"
                        year_preferences[year_range] = year_preferences.get(year_range, 0) + 1
            except Exception as e:
                logger.warning(f"Error processing rating: {str(e)}")
                continue
        
        # Get top genres
        top_genres = sorted(
            genre_preferences.items(),
            key=lambda x: x[1]["avg_rating"],
            reverse=True
        )[:5]
        
        avg_rating = total_rating / len(user_ratings) if user_ratings else 0
        
        return {
            "genre_preferences": {
                genre: {
                    "count": data["count"],
                    "avg_rating": round(data["avg_rating"], 2)
                }
                for genre, data in genre_preferences.items()
            },
            "year_preferences": year_preferences,
            "rating_distribution": rating_distribution,
            "top_genres": [
                {"genre": genre, "avg_rating": round(data[1]["avg_rating"], 2), "count": data[1]["count"]}
                for genre, data in top_genres
            ],
            "average_rating": round(avg_rating, 2),
            "total_ratings": len(user_ratings)
        }
        
    except Exception as e:
        logger.error(f"Error analyzing preferences: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze preferences: {str(e)}")
