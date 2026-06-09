from fastapi import Depends, APIRouter, HTTPException, status, Query, Path
from pydantic import BaseModel
from app.database import get_database
from app.middleware.auth import get_current_user
from app.middleware.rbac import require_role_or_higher, get_permission_list, ROLES
from app.models.user import User
from bson import ObjectId
from typing import Optional, List

router = APIRouter(prefix="/admin", tags=["user-management"])

class UserUpdateRole(BaseModel):
    role: str

class UserResponse(BaseModel):
    user_id: str
    name: str
    email: str
    role: str
    permissions: List[str]

# Define specific routes first (before parameterized routes)

@router.get("/users/roles/all")
async def get_all_roles(
    current_user: User = Depends(require_role_or_higher("moderator")),
):
    """Get all available roles and their permissions (moderator+)."""
    roles_info = {}
    for role_name, role_data in ROLES.items():
        roles_info[role_name] = {
            "description": role_data["description"],
            "permissions": role_data["permissions"],
        }
    
    return {
        "roles": roles_info,
        "current_user_role": current_user.role,
    }

@router.get("/users/stats/overview")
async def get_user_stats(
    current_user: User = Depends(require_role_or_higher("admin")),
):
    """Get user statistics (admin only)."""
    db = get_database()
    
    total_users = await db.users.count_documents({})
    
    # Count users by role
    role_counts = {}
    for role in ROLES.keys():
        count = await db.users.count_documents({"role": role})
        role_counts[role] = count
    
    return {
        "total_users": total_users,
        "by_role": role_counts,
    }

# Generic list/get routes after specific ones

@router.get("/users")
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    role: Optional[str] = None,
    current_user: User = Depends(require_role_or_higher("moderator")),
):
    """List all users (moderator+)."""
    db = get_database()
    
    query = {}
    if role:
        if role not in ROLES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role. Must be one of: {', '.join(ROLES.keys())}"
            )
        query["role"] = role
    
    users_data = await db.users.find(query).skip(skip).limit(limit).to_list(None)
    total = await db.users.count_documents(query)
    
    users = [
        {
            "user_id": str(u["_id"]),
            "name": u.get("name"),
            "email": u.get("email"),
            "role": u.get("role", "user"),
            "permissions": u.get("permissions", []),
        }
        for u in users_data
    ]
    
    return {
        "users": users,
        "total": total,
        "skip": skip,
        "limit": limit,
    }

@router.get("/users/{user_id}")
async def get_user(
    user_id: str = Path(...),
    current_user: User = Depends(require_role_or_higher("moderator")),
):
    """Get user details (moderator+)."""
    db = get_database()
    
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        user = None
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "user_id": str(user["_id"]),
        "name": user.get("name"),
        "email": user.get("email"),
        "role": user.get("role", "user"),
        "permissions": user.get("permissions", []),
        "created_at": user.get("created_at"),
    }

@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: str = Path(...),
    role_data: UserUpdateRole = None,
    current_user: User = Depends(require_role_or_higher("admin")),
):
    """Update user role (admin only)."""
    db = get_database()
    
    if role_data.role not in ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {', '.join(ROLES.keys())}"
        )
    
    try:
        user = await db.users.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "role": role_data.role,
                    "permissions": get_permission_list(role_data.role)
                }
            },
            return_document=True,
        )
    except Exception:
        user = None
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "message": f"User role updated to {role_data.role}",
        "user_id": str(user["_id"]),
        "role": user.get("role"),
        "permissions": user.get("permissions", []),
    }

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str = Path(...),
    current_user: User = Depends(require_role_or_higher("admin")),
):
    """Delete a user (admin only)."""
    db = get_database()
    
    # Prevent self-deletion
    if str(current_user._id) == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    try:
        result = await db.users.delete_one({"_id": ObjectId(user_id)})
    except Exception:
        result = None
    
    if not result or result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Delete user-related data
    await db.favorites.delete_many({"user_id": ObjectId(user_id)})
    await db.ratings.delete_many({"user_id": ObjectId(user_id)})
    await db.reviews.delete_many({"user_id": ObjectId(user_id)})
    await db.wishlists.delete_many({"user_id": ObjectId(user_id)})
    await db.watch_history.delete_many({"user_id": ObjectId(user_id)})
    
    return {"message": "User deleted successfully"}
