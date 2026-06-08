from app.database import get_database
from app.models.rating import Rating
from app.ml.collaborative_filtering import rebuild_model
from bson import ObjectId
from typing import List, Optional

async def add_rating(user_id: str, movie_id: str, rating: float) -> Rating:
    db = get_database()
    existing = await db.ratings.find_one(
        {"user_id": ObjectId(user_id), "movie_id": ObjectId(movie_id)}
    )
    if existing:
        return await update_rating(user_id, movie_id, rating)

    rating_obj = Rating(
        user_id=ObjectId(user_id),
        movie_id=ObjectId(movie_id),
        rating=rating,
    )
    result = await db.ratings.insert_one(rating_obj.to_dict())
    rating_obj._id = result.inserted_id
    
    # Rebuild ML model with new rating data
    try:
        await rebuild_model()
    except Exception as e:
        print(f"Warning: Could not rebuild recommendation model: {e}")
    
    return rating_obj

async def update_rating(user_id: str, movie_id: str, rating: float) -> Rating:
    db = get_database()
    result = await db.ratings.find_one_and_update(
        {"user_id": ObjectId(user_id), "movie_id": ObjectId(movie_id)},
        {"$set": {"rating": rating}},
        return_document=True,
    )
    if result:
        # Rebuild ML model after rating update
        try:
            await rebuild_model()
        except Exception as e:
            print(f"Warning: Could not rebuild recommendation model: {e}")
        
        return Rating.from_dict(result)
    raise ValueError("Rating not found")

async def get_user_ratings(user_id: str) -> List[Rating]:
    db = get_database()
    ratings_data = await db.ratings.find({"user_id": ObjectId(user_id)}).to_list(None)
    return [Rating.from_dict(r) for r in ratings_data]

async def get_rating(user_id: str, movie_id: str) -> Optional[Rating]:
    db = get_database()
    rating_data = await db.ratings.find_one(
        {"user_id": ObjectId(user_id), "movie_id": ObjectId(movie_id)}
    )
    if rating_data:
        return Rating.from_dict(rating_data)
    return None
