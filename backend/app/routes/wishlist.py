from fastapi import Depends, APIRouter, HTTPException, status, Query, Path
from app.services.wishlist_service import (
    add_to_wishlist,
    remove_from_wishlist,
    get_user_wishlist,
    is_in_wishlist,
    update_wishlist_item,
    get_wishlist_by_priority,
    get_wishlist_count,
    get_wishlist_stats,
)
from app.middleware.auth import get_current_user
from app.models.user import User
from typing import Optional

router = APIRouter(prefix="/wishlist", tags=["wishlist"])

@router.post("/add/{movie_id}")
async def add_to_wishlist_route(
    movie_id: str,
    priority: Optional[str] = Query("normal", pattern="^(low|normal|high)$"),
    notes: Optional[str] = Query("", max_length=500),
    current_user: User = Depends(get_current_user),
):
    """Add a movie to user's wishlist."""
    try:
        item = await add_to_wishlist(str(current_user._id), movie_id, priority, notes)
        return {
            "message": "Added to wishlist",
            "wishlist_item": {
                "_id": str(item._id),
                "user_id": str(item.user_id),
                "movie_id": str(item.movie_id),
                "priority": item.priority,
                "notes": item.notes,
                "created_at": item.created_at,
            },
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/remove/{movie_id}")
async def remove_from_wishlist_route(
    movie_id: str,
    current_user: User = Depends(get_current_user),
):
    """Remove a movie from user's wishlist."""
    success = await remove_from_wishlist(str(current_user._id), movie_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist item not found")

    return {"message": "Removed from wishlist"}

@router.get("")
async def get_wishlist(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at", pattern="^(priority|rating|year|title|created_at)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    current_user: User = Depends(get_current_user),
):
    """Get user's wishlist with optional sorting."""
    wishlist, total = await get_user_wishlist(str(current_user._id), skip, limit, sort_by, sort_order)
    return {
        "wishlist": wishlist,
        "total": total,
        "skip": skip,
        "limit": limit,
        "sort_by": sort_by,
        "sort_order": sort_order,
    }

@router.get("/check/{movie_id}")
async def check_wishlist(
    movie_id: str,
    current_user: User = Depends(get_current_user),
):
    """Check if a movie is in user's wishlist."""
    is_in = await is_in_wishlist(str(current_user._id), movie_id)
    return {"is_in_wishlist": is_in}

@router.put("/update/{movie_id}")
async def update_wishlist_item_route(
    movie_id: str,
    priority: Optional[str] = Query(None, pattern="^(low|normal|high)$"),
    notes: Optional[str] = Query(None, max_length=500),
    current_user: User = Depends(get_current_user),
):
    """Update a wishlist item's priority or notes."""
    item = await update_wishlist_item(str(current_user._id), movie_id, priority, notes)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist item not found")

    return {
        "message": "Wishlist item updated",
        "wishlist_item": {
            "_id": str(item._id),
            "user_id": str(item.user_id),
            "movie_id": str(item.movie_id),
            "priority": item.priority,
            "notes": item.notes,
            "created_at": item.created_at,
        },
    }

@router.get("/stats/overview")
async def get_wishlist_stats_route(
    current_user: User = Depends(get_current_user),
):
    """Get wishlist statistics."""
    stats = await get_wishlist_stats(str(current_user._id))
    return {
        "stats": stats,
        "message": "Wishlist statistics",
    }

@router.get("/count/total")
async def get_wishlist_count_route(
    current_user: User = Depends(get_current_user),
):
    """Get total count of wishlist items."""
    count = await get_wishlist_count(str(current_user._id))
    return {
        "count": count,
        "message": "Total wishlist items",
    }

@router.get("/priority/{priority}")
async def get_wishlist_by_priority_route(
    priority: str = Path(..., pattern="^(low|normal|high)$"),
    current_user: User = Depends(get_current_user),
):
    """Get wishlist items filtered by priority."""
    items = await get_wishlist_by_priority(str(current_user._id), priority)
    return {
        "wishlist": items,
        "priority": priority,
        "count": len(items),
    }
