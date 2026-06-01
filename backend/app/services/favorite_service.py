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

async def get_user_favorites(user_id: str, skip: int = 0, limit: int = 10) -> tuple[List[dict], int]:
    db = get_database()
    query = {"user_id": ObjectId(user_id)}
    favorites_data = await db.favorites.find(query).skip(skip).limit(limit).to_list(None)
    total = await db.favorites.count_documents(query)

    favorites = []
    for fav in favorites_data:
        movie = await db.movies.find_one({"_id": fav["movie_id"]})
        if movie:
            movie["_id"] = str(movie["_id"])
            favorites.append(movie)

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
