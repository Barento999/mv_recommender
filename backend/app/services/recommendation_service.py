from app.database import get_database
from app.models.movie import Movie
from bson import ObjectId
from typing import List
from collections import Counter

async def get_recommendations(user_id: str, limit: int = 10) -> List[Movie]:
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
    db = get_database()
    movies_data = await db.movies.find().sort([("rating", -1)]).limit(limit).to_list(None)
    return [Movie.from_dict(m) for m in movies_data]

async def get_similar_movies(movie_id: str, limit: int = 5) -> List[Movie]:
    db = get_database()
    try:
        # Get the target movie
        target_movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
        if not target_movie:
            return []

        # Find movies with similar genres
        target_genres = target_movie.get("genre", [])
        if not target_genres:
            return []

        query = {
            "_id": {"$ne": ObjectId(movie_id)},
            "genre": {"$in": target_genres},
        }

        similar = await db.movies.find(query).sort([("rating", -1)]).limit(limit).to_list(None)
        return [Movie.from_dict(m) for m in similar]
    except Exception:
        return []
