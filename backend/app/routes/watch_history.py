from fastapi import Depends, APIRouter, HTTPException, status, Query
from app.services.watch_history_service import (
    add_to_watch_history,
    get_user_watch_history,
    get_recent_watches,
    clear_watch_history,
    get_watch_history_stats,
    get_most_watched_genres,
    is_movie_watched,
    remove_from_watch_history,
)
from app.middleware.auth import get_current_user
from app.models.user import User
from typing import Optional

router = APIRouter(prefix="/watch-history", tags=["watch-history"])

@router.post("/add/{movie_id}")
async def add_to_history(
    movie_id: str,
    current_user: User = Depends(get_current_user),
):
    """Record that a user watched a movie."""
    try:
        entry = await add_to_watch_history(str(current_user._id), movie_id)
        return {
            "message": "Added to watch history",
            "entry": {
                "_id": str(entry._id),
                "user_id": str(entry.user_id),
                "movie_id": str(entry.movie_id),
                "watched_at": entry.watched_at,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("")
async def get_watch_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
):
    """Get user's watch history."""
    history, total = await get_user_watch_history(str(current_user._id), skip, limit)
    return {
        "history": history,
        "total": total,
        "skip": skip,
        "limit": limit,
    }

@router.get("/recent")
async def get_recent(
    days: int = Query(7, ge=1, le=365),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
):
    """Get movies watched in the last N days."""
    recent = await get_recent_watches(str(current_user._id), days, limit)
    return {
        "recent": recent,
        "days": days,
        "count": len(recent),
    }

@router.get("/check/{movie_id}")
async def check_watched(
    movie_id: str,
    current_user: User = Depends(get_current_user),
):
    """Check if a movie is in watch history."""
    is_watched = await is_movie_watched(str(current_user._id), movie_id)
    return {"is_watched": is_watched}

@router.delete("/remove/{movie_id}")
async def remove_from_history(
    movie_id: str,
    current_user: User = Depends(get_current_user),
):
    """Remove a movie from watch history."""
    success = await remove_from_watch_history(str(current_user._id), movie_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not in history")
    return {"message": "Removed from watch history"}

@router.delete("/clear")
async def clear_history(
    current_user: User = Depends(get_current_user),
):
    """Clear all watch history for the user."""
    success = await clear_watch_history(str(current_user._id))
    return {
        "message": "Watch history cleared",
        "success": success,
    }

@router.get("/stats/overview")
async def get_stats(
    current_user: User = Depends(get_current_user),
):
    """Get watch history statistics."""
    stats = await get_watch_history_stats(str(current_user._id))
    return {
        "stats": stats,
        "message": "Watch history statistics",
    }

@router.get("/genres/most-watched")
async def get_genres(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
):
    """Get most watched genres."""
    genres = await get_most_watched_genres(str(current_user._id), limit)
    return {
        "genres": genres,
        "count": len(genres),
    }
