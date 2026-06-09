from fastapi import Depends, APIRouter, Query
from app.database import get_database
from app.middleware.auth import get_current_user
from app.models.user import User
from app.ml.pipeline import get_recommendation
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/explained")
async def get_recommendations_with_explanations(
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get recommendations with explanations for why they're recommended."""
    try:
        user_id = str(current_user._id)
        user_obj_id = ObjectId(user_id) if isinstance(current_user._id, str) else current_user._id
        
        # Get user's favorites for explanation context
        user_favorites = await db.favorites.find({"user_id": user_obj_id}).to_list(None)
        favorite_movie_ids = [fav["movie_id"] for fav in user_favorites]
        
        # Get favorite movie details for genre analysis
        favorite_movies = []
        if favorite_movie_ids:
            # Convert movie_ids to ObjectId, handling both string and ObjectId formats
            movie_obj_ids = [
                ObjectId(mid) if isinstance(mid, str) and len(mid) == 24 else mid 
                for mid in favorite_movie_ids
            ]
            favorite_movies = await db.movies.find(
                {"_id": {"$in": movie_obj_ids}}
            ).to_list(None)
        
        # Extract genres from favorites
        user_favorite_genres = {}
        for movie in favorite_movies:
            for genre in movie.get("genre", []):
                user_favorite_genres[genre] = user_favorite_genres.get(genre, 0) + 1
        
        # Get ML recommendations
        ml_recommendations = await get_recommendation(user_id, limit=limit, model_type="cf")
        
        if not ml_recommendations:
            return {
                "recommendations": [],
                "explanations": [],
                "count": 0,
                "message": "No recommendations available"
            }
        
        # Build recommendations with explanations
        movie_ids = [
            ObjectId(movie_id) if isinstance(movie_id, str) and len(movie_id) == 24 else movie_id 
            for movie_id, _ in ml_recommendations
        ]
        movies_data = await db.movies.find({"_id": {"$in": movie_ids}}).to_list(None)
        
        recommendations_with_explanations = []
        movies_map = {str(m["_id"]): m for m in movies_data}
        
        for idx, (movie_id, score) in enumerate(ml_recommendations):
            if movie_id in movies_map:
                movie = movies_map[movie_id]
                explanation = _generate_explanation(movie, user_favorite_genres, score, idx + 1)
                
                recommendations_with_explanations.append({
                    "_id": str(movie["_id"]),
                    "title": movie.get("title", "Unknown"),
                    "genre": movie.get("genre", []),
                    "year": movie.get("year", 0),
                    "rating": movie.get("rating", 0),
                    "description": movie.get("description", ""),
                    "poster_url": movie.get("poster_url", ""),
                    "trailer_url": movie.get("trailer_url", ""),
                    "created_at": movie.get("created_at", ""),
                    "explanation": explanation
                })
        
        return {
            "recommendations": recommendations_with_explanations,
            "count": len(recommendations_with_explanations),
            "total_favorites": len(favorite_movies),
            "message": f"Personalized recommendations based on your {len(favorite_movies)} favorite movies"
        }
        
    except Exception as e:
        logger.error(f"Error getting recommendations with explanations: {str(e)}")
        return {
            "recommendations": [],
            "explanations": [],
            "count": 0,
            "error": str(e),
            "message": "Failed to generate recommendations"
        }


def _generate_explanation(movie: Dict, user_favorite_genres: Dict, score: float, rank: int) -> Dict:
    """Generate explanation for why a movie is recommended."""
    explanation_parts = []
    explanation_type = "Unknown"
    confidence = min(int(score * 100), 100)  # Score as percentage
    
    # Check genre match
    movie_genres = movie.get("genre", [])
    matching_genres = [g for g in movie_genres if g in user_favorite_genres]
    
    if matching_genres:
        explanation_type = "Genre Match"
        top_genre = matching_genres[0]
        count = user_favorite_genres.get(top_genre, 0)
        explanation_parts.append(f"Matches your interest in {top_genre}")
        if count > 1:
            explanation_parts.append(f"(you favorited {count} {top_genre} movies)")
    
    # Check rating
    movie_rating = movie.get("rating", 0)
    if movie_rating >= 7.5:
        explanation_type = "High Rated"
        explanation_parts.append(f"Highly rated ({movie_rating}/10)")
    
    # Check year
    movie_year = movie.get("year", 0)
    if movie_year and movie_year >= 2020:
        explanation_type = "Recent & Popular"
        explanation_parts.append(f"Recent release ({movie_year})")
    
    # Combine explanations
    if not explanation_parts:
        explanation_parts = ["Similar to movies you like"]
        explanation_type = "Collaborative"
    
    return {
        "type": explanation_type,
        "reasons": explanation_parts,
        "confidence": confidence,
        "rank": rank
    }


@router.get("/explanation/{movie_id}")
async def get_movie_explanation(
    movie_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get detailed explanation for why a specific movie is recommended to the user."""
    try:
        user_id = str(current_user._id)
        user_obj_id = ObjectId(user_id) if isinstance(current_user._id, str) else current_user._id
        
        # Get the movie - handle ObjectId conversion safely
        try:
            movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
        except Exception:
            movie = None
        if not movie:
            return {"error": "Movie not found"}
        
        # Get user's favorites
        user_favorites = await db.favorites.find({"user_id": user_obj_id}).to_list(None)
        favorite_movie_ids = [fav["movie_id"] for fav in user_favorites]
        
        # Get favorite movie details
        favorite_movies = []
        if favorite_movie_ids:
            # Convert movie_ids to ObjectId, handling both string and ObjectId formats
            movie_obj_ids = [
                ObjectId(mid) if isinstance(mid, str) and len(mid) == 24 else mid 
                for mid in favorite_movie_ids
            ]
            favorite_movies = await db.movies.find(
                {"_id": {"$in": movie_obj_ids}}
            ).to_list(None)
        
        # Extract genres and analysis
        user_favorite_genres = {}
        for fav_movie in favorite_movies:
            for genre in fav_movie.get("genre", []):
                user_favorite_genres[genre] = user_favorite_genres.get(genre, 0) + 1
        
        # Get user's ratings for context
        user_ratings = await db.ratings.find(
            {"user_id": user_obj_id},
            {"movie_id": 1, "rating": 1}
        ).to_list(None)
        
        avg_user_rating = 0
        if user_ratings:
            avg_user_rating = sum(r["rating"] for r in user_ratings) / len(user_ratings)
        
        # Build detailed explanation
        movie_genres = movie.get("genre", [])
        matching_genres = [g for g in movie_genres if g in user_favorite_genres]
        
        recommendation_factors = {
            "genre_match": {
                "matched": matching_genres,
                "total_user_genres": len(user_favorite_genres),
                "score": len(matching_genres) / max(len(movie_genres), 1) * 100
            },
            "rating_analysis": {
                "movie_rating": movie.get("rating", 0),
                "user_average_rating": round(avg_user_rating, 2),
                "difference": round(movie.get("rating", 0) - avg_user_rating, 2)
            },
            "user_context": {
                "favorite_movies_count": len(favorite_movies),
                "total_ratings": len(user_ratings),
                "favorite_genres": dict(sorted(user_favorite_genres.items(), key=lambda x: x[1], reverse=True)[:5])
            }
        }
        
        return {
            "movie_id": str(movie["_id"]),
            "title": movie.get("title", "Unknown"),
            "recommendation_factors": recommendation_factors,
            "summary": f"This movie shares genres with your favorite movies and has a rating of {movie.get('rating', 0)}/10"
        }
        
    except Exception as e:
        logger.error(f"Error getting movie explanation: {str(e)}")
        return {"error": str(e)}
