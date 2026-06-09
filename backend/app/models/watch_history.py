from datetime import datetime
from typing import Optional
from bson import ObjectId

class WatchHistory:
    def __init__(
        self,
        user_id: ObjectId,
        movie_id: ObjectId,
        watched_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None,
    ):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.movie_id = movie_id
        self.watched_at = watched_at or datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "watched_at": self.watched_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "WatchHistory":
        return WatchHistory(
            user_id=data.get("user_id"),
            movie_id=data.get("movie_id"),
            watched_at=data.get("watched_at"),
            _id=data.get("_id"),
        )
