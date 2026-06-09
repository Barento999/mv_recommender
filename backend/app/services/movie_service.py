from app.database import get_database
from app.models.movie import Movie
from bson import ObjectId
from typing import List, Optional
from pymongo import ASCENDING

async def create_movie(
    title: str,
    genre: List[str],
    year: int,
    rating: float,
    description: str,
    poster_url: str,
    trailer_url: Optional[str] = None,
) -> Movie:
    db = get_database()
    movie = Movie(
        title=title,
        genre=genre,
        year=year,
        rating=rating,
        description=description,
        poster_url=poster_url,
        trailer_url=trailer_url,
    )
    result = await db.movies.insert_one(movie.to_dict())
    movie._id = result.inserted_id
    return movie

async def get_movie_by_id(movie_id: str) -> Optional[Movie]:
    db = get_database()
    try:
        movie_data = await db.movies.find_one({"_id": ObjectId(movie_id)})
        if movie_data:
            return Movie.from_dict(movie_data)
    except Exception:
        pass
    return None

async def get_all_movies(
    skip: int = 0, 
    limit: int = 10, 
    genre: Optional[str] = None, 
    year: Optional[int] = None,
    sort_by: Optional[str] = "rating",
    sort_order: Optional[str] = "desc",
) -> tuple[List[Movie], int]:
    db = get_database()
    query = {}

    if genre:
        query["genre"] = genre

    if year:
        query["year"] = year

    # Determine sort direction
    sort_direction = -1 if sort_order == "desc" else 1
    
    # Map sort_by to database field
    sort_field_map = {
        "rating": "rating",
        "year": "year",
        "title": "title"
    }
    sort_field = sort_field_map.get(sort_by, "rating")

    movies_data = await db.movies.find(query).sort(sort_field, sort_direction).skip(skip).limit(limit).to_list(None)
    total = await db.movies.count_documents(query)

    movies = [Movie.from_dict(m) for m in movies_data]
    return movies, total

async def search_movies(
    query: str, 
    skip: int = 0, 
    limit: int = 10,
    sort_by: Optional[str] = "rating",
    sort_order: Optional[str] = "desc",
) -> tuple[List[Movie], int]:
    db = get_database()
    search_query = {
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}},
        ]
    }
    
    # Determine sort direction
    sort_direction = -1 if sort_order == "desc" else 1
    
    # Map sort_by to database field
    sort_field_map = {
        "rating": "rating",
        "year": "year",
        "title": "title"
    }
    sort_field = sort_field_map.get(sort_by, "rating")
    
    movies_data = await db.movies.find(search_query).sort(sort_field, sort_direction).skip(skip).limit(limit).to_list(None)
    total = await db.movies.count_documents(search_query)

    movies = [Movie.from_dict(m) for m in movies_data]
    return movies, total

async def filter_movies_by_rating(
    min_rating: float, skip: int = 0, limit: int = 10
) -> tuple[List[Movie], int]:
    db = get_database()
    query = {"rating": {"$gte": min_rating}}
    movies_data = await db.movies.find(query).skip(skip).limit(limit).to_list(None)
    total = await db.movies.count_documents(query)

    movies = [Movie.from_dict(m) for m in movies_data]
    return movies, total

async def update_movie(movie_id: str, update_data: dict) -> Optional[Movie]:
    db = get_database()
    try:
        result = await db.movies.find_one_and_update(
            {"_id": ObjectId(movie_id)},
            {"$set": update_data},
            return_document=True,
        )
        if result:
            return Movie.from_dict(result)
    except Exception:
        pass
    return None

async def delete_movie(movie_id: str) -> bool:
    db = get_database()
    try:
        result = await db.movies.delete_one({"_id": ObjectId(movie_id)})
        return result.deleted_count > 0
    except Exception:
        return False
