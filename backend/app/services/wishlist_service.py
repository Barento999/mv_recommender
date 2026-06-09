from app.database import get_database
from app.models.wishlist import Wishlist
from bson import ObjectId
from typing import List, Optional

async def add_to_wishlist(user_id: str, movie_id: str, priority: str = "normal", notes: str = "") -> Wishlist:
    """Add a movie to user's wishlist."""
    db = get_database()
    
    # Check if already in wishlist
    existing = await db.wishlists.find_one(
        {"user_id": ObjectId(user_id), "movie_id": ObjectId(movie_id)}
    )
    if existing:
        raise ValueError("Already in wishlist")

    wishlist = Wishlist(
        user_id=ObjectId(user_id), 
        movie_id=ObjectId(movie_id),
        priority=priority,
        notes=notes
    )
    result = await db.wishlists.insert_one(wishlist.to_dict())
    wishlist._id = result.inserted_id
    return wishlist

async def remove_from_wishlist(user_id: str, movie_id: str) -> bool:
    """Remove a movie from user's wishlist."""
    db = get_database()
    try:
        result = await db.wishlists.delete_one(
            {"user_id": ObjectId(user_id), "movie_id": ObjectId(movie_id)}
        )
        return result.deleted_count > 0
    except Exception:
        return False

async def get_user_wishlist(
    user_id: str, 
    skip: int = 0, 
    limit: int = 10, 
    sort_by: str = "created_at", 
    sort_order: str = "desc"
) -> tuple[List[dict], int]:
    """Get user's wishlist with optional sorting."""
    db = get_database()
    query = {"user_id": ObjectId(user_id)}
    
    # Determine sort direction
    sort_direction = -1 if sort_order == "desc" else 1
    
    # Map sort_by to database field (sort by movie attributes)
    sort_field_map = {
        "priority": "priority",
        "rating": "rating",
        "year": "year",
        "title": "title",
        "created_at": "_id"
    }
    sort_field = sort_field_map.get(sort_by, "created_at")
    
    # Get wishlist records
    wishlist_data = await db.wishlists.find(query).skip(skip).limit(limit).to_list(None)
    total = await db.wishlists.count_documents(query)

    wishlist = []
    movie_with_sort_data = []
    
    for wl in wishlist_data:
        movie = await db.movies.find_one({"_id": wl["movie_id"]})
        if movie:
            movie["_id"] = str(movie["_id"])
            movie["wishlist_priority"] = wl.get("priority", "normal")
            movie["wishlist_notes"] = wl.get("notes", "")
            movie["wishlist_id"] = str(wl["_id"])
            movie["wishlist_added_at"] = wl.get("created_at")
            movie_with_sort_data.append((movie, movie.get(sort_field, 0)))
    
    # Sort by the specified field
    movie_with_sort_data.sort(key=lambda x: x[1], reverse=(sort_order == "desc"))
    
    wishlist = [movie for movie, _ in movie_with_sort_data]

    return wishlist, total

async def is_in_wishlist(user_id: str, movie_id: str) -> bool:
    """Check if a movie is in user's wishlist."""
    db = get_database()
    try:
        result = await db.wishlists.find_one(
            {"user_id": ObjectId(user_id), "movie_id": ObjectId(movie_id)}
        )
        return result is not None
    except Exception:
        return False

async def update_wishlist_item(
    user_id: str, 
    movie_id: str, 
    priority: Optional[str] = None,
    notes: Optional[str] = None
) -> Optional[Wishlist]:
    """Update a wishlist item's priority or notes."""
    db = get_database()
    try:
        update_data = {}
        if priority:
            update_data["priority"] = priority
        if notes is not None:
            update_data["notes"] = notes
        
        if not update_data:
            return None
        
        result = await db.wishlists.find_one_and_update(
            {"user_id": ObjectId(user_id), "movie_id": ObjectId(movie_id)},
            {"$set": update_data},
            return_document=True,
        )
        if result:
            return Wishlist.from_dict(result)
    except Exception:
        pass
    return None

async def get_wishlist_by_priority(
    user_id: str, 
    priority: str
) -> List[dict]:
    """Get wishlist items filtered by priority."""
    db = get_database()
    query = {"user_id": ObjectId(user_id), "priority": priority}
    
    wishlist_data = await db.wishlists.find(query).to_list(None)
    
    wishlist = []
    for wl in wishlist_data:
        movie = await db.movies.find_one({"_id": wl["movie_id"]})
        if movie:
            movie["_id"] = str(movie["_id"])
            movie["wishlist_priority"] = wl.get("priority", "normal")
            movie["wishlist_notes"] = wl.get("notes", "")
            movie["wishlist_id"] = str(wl["_id"])
            wishlist.append(movie)
    
    return wishlist

async def get_wishlist_count(user_id: str) -> int:
    """Get total count of wishlist items for a user."""
    db = get_database()
    return await db.wishlists.count_documents({"user_id": ObjectId(user_id)})

async def get_wishlist_stats(user_id: str) -> dict:
    """Get wishlist statistics for a user."""
    db = get_database()
    query = {"user_id": ObjectId(user_id)}
    
    total = await db.wishlists.count_documents(query)
    low = await db.wishlists.count_documents({**query, "priority": "low"})
    normal = await db.wishlists.count_documents({**query, "priority": "normal"})
    high = await db.wishlists.count_documents({**query, "priority": "high"})
    
    return {
        "total": total,
        "low_priority": low,
        "normal_priority": normal,
        "high_priority": high,
    }
