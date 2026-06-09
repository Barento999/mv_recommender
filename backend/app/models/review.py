from datetime import datetime
from typing import Optional
from bson import ObjectId

class Review:
    def __init__(
        self,
        user_id: ObjectId,
        movie_id: ObjectId,
        rating: int,
        title: str,
        content: str,
        helpful_count: int = 0,
        _id: Optional[ObjectId] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating  # 1-10
        self.title = title
        self.content = content
        self.helpful_count = helpful_count
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "rating": self.rating,
            "title": self.title,
            "content": self.content,
            "helpful_count": self.helpful_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "Review":
        return Review(
            user_id=data.get("user_id"),
            movie_id=data.get("movie_id"),
            rating=data.get("rating"),
            title=data.get("title"),
            content=data.get("content"),
            helpful_count=data.get("helpful_count", 0),
            _id=data.get("_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
