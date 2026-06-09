from datetime import datetime
from typing import Optional
from bson import ObjectId

class Wishlist:
    def __init__(
        self,
        user_id: ObjectId,
        movie_id: ObjectId,
        priority: Optional[str] = "normal",
        notes: Optional[str] = None,
        _id: Optional[ObjectId] = None,
        created_at: Optional[datetime] = None,
    ):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.movie_id = movie_id
        self.priority = priority or "normal"  # low, normal, high
        self.notes = notes or ""
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "priority": self.priority,
            "notes": self.notes,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "Wishlist":
        return Wishlist(
            user_id=data.get("user_id"),
            movie_id=data.get("movie_id"),
            priority=data.get("priority", "normal"),
            notes=data.get("notes", ""),
            _id=data.get("_id"),
            created_at=data.get("created_at"),
        )
