from fastapi import HTTPException, status, Depends
from app.middleware.auth import get_current_user
from app.models.user import User
from typing import List

# Role definitions
ROLES = {
    "user": {
        "description": "Regular user",
        "permissions": [
            "read_movies",
            "rate_movies",
            "add_favorites",
            "write_reviews",
            "view_recommendations",
            "manage_wishlist",
            "view_watch_history",
            "view_preferences",
        ]
    },
    "moderator": {
        "description": "Content moderator",
        "permissions": [
            "read_movies",
            "rate_movies",
            "add_favorites",
            "write_reviews",
            "view_recommendations",
            "manage_wishlist",
            "view_watch_history",
            "view_preferences",
            "delete_reviews",  # Delete inappropriate reviews
            "edit_movies",  # Edit movie metadata
            "view_analytics",  # Limited analytics
            "moderate_reviews",  # Flag reviews
        ]
    },
    "admin": {
        "description": "Administrator",
        "permissions": [
            # All permissions
            "read_movies",
            "rate_movies",
            "add_favorites",
            "write_reviews",
            "view_recommendations",
            "manage_wishlist",
            "view_watch_history",
            "view_preferences",
            "delete_reviews",
            "edit_movies",
            "view_analytics",
            "moderate_reviews",
            "manage_users",  # Create, delete, update users
            "manage_roles",  # Assign/revoke roles
            "view_system_analytics",  # Full system analytics
            "manage_movies",  # Create, delete movies
            "manage_content",  # Full content management
        ]
    }
}

def check_permission(required_permission: str):
    """Check if user has required permission."""
    async def dependency(current_user: User = Depends(get_current_user)):
        user_role = current_user.role
        
        if user_role not in ROLES:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid user role"
            )
        
        role_permissions = ROLES[user_role]["permissions"]
        
        if required_permission not in role_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {required_permission}"
            )
        
        return current_user
    return dependency

def check_permissions(required_permissions: List[str]):
    """Check if user has all required permissions."""
    async def dependency(current_user: User = Depends(get_current_user)):
        user_role = current_user.role
        
        if user_role not in ROLES:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid user role"
            )
        
        role_permissions = ROLES[user_role]["permissions"]
        
        missing_permissions = [
            perm for perm in required_permissions
            if perm not in role_permissions
        ]
        
        if missing_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permissions: {', '.join(missing_permissions)}"
            )
        
        return current_user
    return dependency

def require_role(required_role: str):
    """Check if user has required role."""
    async def dependency(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This endpoint requires '{required_role}' role"
            )
        
        return current_user
    return dependency

def require_role_or_higher(required_role: str):
    """Check if user has required role or higher (admin > moderator > user)."""
    async def dependency(current_user: User = Depends(get_current_user)):
        role_hierarchy = {"user": 0, "moderator": 1, "admin": 2}
        
        user_level = role_hierarchy.get(current_user.role, -1)
        required_level = role_hierarchy.get(required_role, -1)
        
        if user_level < required_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This endpoint requires '{required_role}' role or higher"
            )
        
        return current_user
    return dependency

def get_permission_list(role: str) -> List[str]:
    """Get list of permissions for a role."""
    return ROLES.get(role, {}).get("permissions", [])

def get_role_description(role: str) -> str:
    """Get description of a role."""
    return ROLES.get(role, {}).get("description", "Unknown role")
