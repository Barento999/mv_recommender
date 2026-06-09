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
        
        if ml_recommendations and len(ml_recommendations) > 0:
            # Convert movie IDs to Movie objects
            try:
                movie_ids = [
                    ObjectId(movie_id) if isinstance(movie_id, str) and len(movie_id) == 24 else movie_id
                    for movie_id, _ in ml_recommendations
                ]
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
                logger.warning(f"Error processing ML recommendations: {str(e)}")
    
    except Exception as e:
        logger.warning(f"ML recommendation failed: {str(e)}")
    
    # Fallback to genre-based recommendations
    logger.info(f"Falling back to genre-based recommendations for {user_id}")
    return await get_recommendations_fallback(user_id, limit)

async def get_recommendations_fallback(user_id: str, limit: int = 10) -> List[Movie]:
    """
    Fallback recommendation using:
    1. User's favorite movies genres (if user has favorites)
    2. User's rated movies genres (if user has ratings)
    3. Top-rated movies (if user has no activity)
    """
    db = get_database()
    
    try:
        user_obj_id = ObjectId(user_id) if isinstance(user_id, str) and len(user_id) == 24 else user_id
    except Exception:
        user_obj_id = user_id

    # Try to get user's favorite movies first
    favorites = await db.favorites.find({"user_id": user_obj_id}).to_list(None)
    favorite_movie_ids = [fav["movie_id"] for fav in favorites]
    
    # If no favorites, try to get user's rated movies
    if not favorite_movie_ids:
        ratings = await db.ratings.find({"user_id": user_obj_id}).to_list(None)
        favorite_movie_ids = [r["movie_id"] for r in ratings if r.get("rating", 0) >= 7]
    
    # If still nothing, return top-rated movies
    if not favorite_movie_ids:
        logger.info(f"No user activity found for {user_id}, returning top-rated movies")
        return await get_top_rated_movies(limit)

    # Get favorite/highly-rated movie details
    favorite_movies = await db.movies.find({"_id": {"$in": favorite_movie_ids}}).to_list(None)

    # Count genre frequency
    genre_counter = Counter()
    for movie in favorite_movies:
        for genre in movie.get("genre", []):
            genre_counter[genre] += 1

    if not genre_counter:
        return await get_top_rated_movies(limit)

    # Get top genres
    top_genres = [genre for genre, _ in genre_counter.most_common(5)]
    logger.info(f"User {user_id} top genres: {top_genres}")

    # Find movies with similar genres, excluding already watched/rated movies
    query = {
        "_id": {"$nin": favorite_movie_ids},
        "genre": {"$in": top_genres},
    }

    recommendations = await db.movies.find(query).sort([("rating", -1)]).limit(limit).to_list(None)
    
    if not recommendations:
        # Fallback if no genre matches
        logger.info(f"No genre matches, returning top-rated movies")
        recommendations = await db.movies.find({"_id": {"$nin": favorite_movie_ids}}).sort([("rating", -1)]).limit(limit).to_list(None)
    
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
            try:
                movie_ids = [
                    ObjectId(mid) if isinstance(mid, str) and len(mid) == 24 else mid
                    for mid, _ in similar_from_ml
                ]
                movies_data = await db.movies.find({"_id": {"$in": movie_ids}}).to_list(None)
                if movies_data:
                    return [Movie.from_dict(m) for m in movies_data]
            except Exception as e:
                logger.warning(f"Error processing ML similar movies: {str(e)}")
    
    except Exception as e:
        logger.warning(f"ML similar movies failed: {str(e)}")
    
    # Fallback: Get the target movie and find similar by genre
    try:
        try:
            target_movie_id = ObjectId(movie_id) if isinstance(movie_id, str) and len(movie_id) == 24 else movie_id
        except Exception:
            target_movie_id = movie_id
            
        target_movie = await db.movies.find_one({"_id": target_movie_id})
        if not target_movie:
            return []

        target_genres = target_movie.get("genre", [])
        if not target_genres:
            return []

        query = {
            "_id": {"$ne": target_movie_id},
            "genre": {"$in": target_genres},
        }

        similar = await db.movies.find(query).sort([("rating", -1)]).limit(limit).to_list(None)
        return [Movie.from_dict(m) for m in similar]
    
    except Exception as e:
        logger.error(f"Similar movies fallback failed: {str(e)}")
        return []
