from app.database import get_database
from app.models.movie import Movie
from app.ml.pipeline import get_recommendation, get_similar_movies as get_similar_from_pipeline, get_model
from bson import ObjectId
from typing import List
from collections import Counter
import logging

logger = logging.getLogger(__name__)

async def get_recommendations(user_id: str, limit: int = 10) -> List[Movie]:
    """
    Get personalized movie recommendations using ML pipeline
    
    Uses collaborative filtering model trained on application startup.
    Falls back to genre-based recommendations if ML fails.
    """
    db = get_database()
    
    try:
        # Get ML-based recommendations from pipeline
        logger.info(f"Getting ML recommendations for {user_id}")
        ml_recommendations = await get_recommendation(user_id, limit=limit, model_type="cf")
        
        if ml_recommendations:
            # Convert movie IDs to Movie objects
            movie_ids = [ObjectId(movie_id) for movie_id, _ in ml_recommendations]
            movies_data = await db.movies.find({"_id": {"$in": movie_ids}}).to_list(None)
            
            if movies_data:
                # Create a mapping for efficient lookup
                movies_map = {str(m["_id"]): m for m in movies_data}
                
                # Return in order of predicted scores
                recommendations = []
                for movie_id, score in ml_recommendations:
                    if movie_id in movies_map:
                        recommendations.append(Movie.from_dict(movies_map[movie_id]))
                
                if recommendations:
                    logger.info(f"✓ Returned {len(recommendations)} ML recommendations")
                    return recommendations
    
    except Exception as e:
        logger.warning(f"ML recommendation failed: {str(e)}")
    
    # Fallback to genre-based recommendations
    logger.info(f"Falling back to genre-based recommendations for {user_id}")
    return await get_recommendations_fallback(user_id, limit)

async def get_recommendations_fallback(user_id: str, limit: int = 10) -> List[Movie]:
    """
    Fallback recommendation using genre-based collaborative filtering
    """
    db = get_database()

    # Get user's favorite movies
    favorites = await db.favorites.find({"user_id": ObjectId(user_id)}).to_list(None)
    if not favorites:
        # No favorites, return top-rated movies
        return await get_top_rated_movies(limit)

    # Extract genres from favorite movies
    favorite_movie_ids = [fav["movie_id"] for fav in favorites]
    favorite_movies = await db.movies.find({"_id": {"$in": favorite_movie_ids}}).to_list(None)

    # Count genre frequency
    genre_counter = Counter()
    for movie in favorite_movies:
        for genre in movie.get("genre", []):
            genre_counter[genre] += 1

    if not genre_counter:
        return await get_top_rated_movies(limit)

    # Get top genres
    top_genres = [genre for genre, _ in genre_counter.most_common(3)]

    # Find movies with similar genres, excluding watched/favorited movies
    query = {
        "_id": {"$nin": favorite_movie_ids},
        "genre": {"$in": top_genres},
    }

    recommendations = await db.movies.find(query).sort([("rating", -1)]).limit(limit).to_list(None)
    return [Movie.from_dict(m) for m in recommendations]

async def get_top_rated_movies(limit: int = 10) -> List[Movie]:
    """Get top-rated movies as fallback."""
    db = get_database()
    movies_data = await db.movies.find().sort([("rating", -1)]).limit(limit).to_list(None)
    return [Movie.from_dict(m) for m in movies_data]

async def get_similar_movies(movie_id: str, limit: int = 5) -> List[Movie]:
    """
    Get movies similar to a given movie using ML pipeline
    
    Uses content-based recommendations if available.
    Falls back to genre-based similarity.
    """
    db = get_database()
    try:
        # Try ML-based similar movies first
        similar_from_ml = await get_similar_from_pipeline(movie_id, limit=limit)
        
        if similar_from_ml:
            movie_ids = [ObjectId(movie_id) for movie_id, _ in similar_from_ml]
            movies_data = await db.movies.find({"_id": {"$in": movie_ids}}).to_list(None)
            if movies_data:
                return [Movie.from_dict(m) for m in movies_data]
    
    except Exception as e:
        logger.warning(f"ML similar movies failed: {str(e)}")
    
    # Fallback: Get the target movie and find similar by genre
    try:
        target_movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
        if not target_movie:
            return []

        target_genres = target_movie.get("genre", [])
        if not target_genres:
            return []

        query = {
            "_id": {"$ne": ObjectId(movie_id)},
            "genre": {"$in": target_genres},
        }

        similar = await db.movies.find(query).sort([("rating", -1)]).limit(limit).to_list(None)
        return [Movie.from_dict(m) for m in similar]
    
    except Exception as e:
        logger.error(f"Similar movies fallback failed: {str(e)}")
        return []
