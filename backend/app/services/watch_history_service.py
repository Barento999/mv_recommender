from app.database import get_database
from app.models.watch_history import WatchHistory
from bson import ObjectId
from typing import List, Optional
from datetime import datetime, timedelta

async def add_to_watch_history(user_id: str, movie_id: str) -> WatchHistory:
    """Add a movie to user's watch history."""
    db = get_database()
    
    # Check if movie is already in history (within last 5 minutes to avoid duplicates)
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
    existing = await db.watch_history.find_one({
        "user_id": ObjectId(user_id), 
        "movie_id": ObjectId(movie_id),
        "watched_at": {"$gt": five_minutes_ago}
    })
    
    if existing:
        # Update the watched_at timestamp instead of creating a duplicate
        result = await db.watch_history.find_one_and_update(
            {"_id": existing["_id"]},
            {"$set": {"watched_at": datetime.utcnow()}},
            return_document=True,
        )
        return WatchHistory.from_dict(result)

    # Create new watch history entry
    watch_entry = WatchHistory(user_id=ObjectId(user_id), movie_id=ObjectId(movie_id))
    result = await db.watch_history.insert_one(watch_entry.to_dict())
    watch_entry._id = result.inserted_id
    return watch_entry

async def get_user_watch_history(
    user_id: str, 
    skip: int = 0, 
    limit: int = 10,
) -> tuple[List[dict], int]:
    """Get user's watch history with most recent first."""
    db = get_database()
    query = {"user_id": ObjectId(user_id)}
    
    # Get watch history records (most recent first)
    history_data = await db.watch_history.find(query).sort("watched_at", -1).skip(skip).limit(limit).to_list(None)
    total = await db.watch_history.count_documents(query)

    watch_history = []
    
    for entry in history_data:
        movie = await db.movies.find_one({"_id": entry["movie_id"]})
        if movie:
            movie["_id"] = str(movie["_id"])
            movie["watched_at"] = entry.get("watched_at")
            watch_history.append(movie)

    return watch_history, total

async def get_recent_watches(user_id: str, days: int = 7, limit: int = 10) -> List[dict]:
    """Get movies watched in the last N days."""
    db = get_database()
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    query = {
        "user_id": ObjectId(user_id),
        "watched_at": {"$gte": cutoff_date}
    }
    
    history_data = await db.watch_history.find(query).sort("watched_at", -1).limit(limit).to_list(None)

    watch_history = []
    
    for entry in history_data:
        movie = await db.movies.find_one({"_id": entry["movie_id"]})
        if movie:
            movie["_id"] = str(movie["_id"])
            movie["watched_at"] = entry.get("watched_at")
            watch_history.append(movie)

    return watch_history

async def clear_watch_history(user_id: str) -> bool:
    """Clear all watch history for a user."""
    db = get_database()
    try:
        result = await db.watch_history.delete_many({"user_id": ObjectId(user_id)})
        return result.deleted_count > 0
    except Exception:
        return False

async def get_watch_history_stats(user_id: str) -> dict:
    """Get watch history statistics."""
    db = get_database()
    query = {"user_id": ObjectId(user_id)}
    
    total = await db.watch_history.count_documents(query)
    
    # Get stats for different time periods
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    today_count = await db.watch_history.count_documents({
        **query,
        "watched_at": {"$gte": today}
    })
    
    week_count = await db.watch_history.count_documents({
        **query,
        "watched_at": {"$gte": week_ago}
    })
    
    month_count = await db.watch_history.count_documents({
        **query,
        "watched_at": {"$gte": month_ago}
    })
    
    return {
        "total": total,
        "today": today_count,
        "this_week": week_count,
        "this_month": month_count,
    }

async def get_most_watched_genres(user_id: str, limit: int = 10) -> dict:
    """Get genres from movies in watch history."""
    db = get_database()
    
    history_data = await db.watch_history.find({"user_id": ObjectId(user_id)}).to_list(None)
    
    genre_count = {}
    
    for entry in history_data:
        movie = await db.movies.find_one({"_id": entry["movie_id"]})
        if movie:
            for genre in movie.get("genre", []):
                genre_count[genre] = genre_count.get(genre, 0) + 1
    
    # Sort by count descending
    sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)
    return {genre: count for genre, count in sorted_genres[:limit]}

async def is_movie_watched(user_id: str, movie_id: str) -> bool:
    """Check if a movie is in user's watch history."""
    db = get_database()
    try:
        result = await db.watch_history.find_one({
            "user_id": ObjectId(user_id),
            "movie_id": ObjectId(movie_id)
        })
        return result is not None
    except Exception:
        return False

async def remove_from_watch_history(user_id: str, movie_id: str) -> bool:
    """Remove a movie from watch history."""
    db = get_database()
    try:
        result = await db.watch_history.delete_one({
            "user_id": ObjectId(user_id),
            "movie_id": ObjectId(movie_id)
        })
        return result.deleted_count > 0
    except Exception:
        return False
