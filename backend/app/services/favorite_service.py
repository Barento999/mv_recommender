from app.database import get_database
from app.models.favorite import Favorite
from bson import ObjectId
from typing import List, Optional

async def add_favorite(user_id: str, movie_id: str) -> Favorite:
    db = get_database()
    existing = await db.favorites.find_one(
        {"user_id": ObjectId(user_id), "movie_id": ObjectId(movie_id)}
    )
    if existing:
        raise ValueError("Already in favorites")

    favorite = Favorite(user_id=ObjectId(user_id), movie_id=ObjectId(movie_id))
    result = await db.favorites.insert_one(favorite.to_dict())
    favorite._id = result.inserted_id
    return favorite

async def remove_favorite(user_id: str, movie_id: str) -> bool:
    db = get_database()
    try:
        result = await db.favorites.delete_one(
            {"user_id": ObjectId(user_id), "movie_id": ObjectId(movie_id)}
        )
        return result.deleted_count > 0
    except Exception:
        return False

async def get_user_favorites(user_id: str, skip: int = 0, limit: int = 10, sort_by: str = "created_at", sort_order: str = "desc") -> tuple[List[dict], int]:
    db = get_database()
    query = {"user_id": ObjectId(user_id)}
    
    # Determine sort direction
    sort_direction = -1 if sort_order == "desc" else 1
    
    # Map sort_by to database field (sort by movie attributes)
    sort_field_map = {
        "rating": "rating",
        "year": "year",
        "title": "title",
        "created_at": "_id"  # Use _id as proxy for creation time
    }
    sort_field = sort_field_map.get(sort_by, "rating")
    
    # For movie attributes, we need to aggregate to get the data correctly
    # First get favorite records, then sort the movies
    favorites_data = await db.favorites.find(query).skip(skip).limit(limit).to_list(None)
    total = await db.favorites.count_documents(query)

    favorites = []
    movie_with_sort_data = []
    
    for fav in favorites_data:
        movie = await db.movies.find_one({"_id": fav["movie_id"]})
        if movie:
            movie["_id"] = str(movie["_id"])
            movie_with_sort_data.append((movie, movie.get(sort_field, 0)))
    
    # Sort by the specified field
    movie_with_sort_data.sort(key=lambda x: x[1], reverse=(sort_order == "desc"))
    
    favorites = [movie for movie, _ in movie_with_sort_data]

    return favorites, total

async def is_favorite(user_id: str, movie_id: str) -> bool:
    db = get_database()
    try:
        result = await db.favorites.find_one(
            {"user_id": ObjectId(user_id), "movie_id": ObjectId(movie_id)}
        )
        return result is not None
    except Exception:
        return False
