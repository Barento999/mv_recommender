from datetime import datetime
from typing import Optional, List
from bson import ObjectId

class Movie:
    def __init__(
        self,
        title: str,
        genre: List[str],
        year: int,
        rating: float,
        description: str,
        poster_url: str,
        trailer_url: Optional[str] = None,
        _id: Optional[ObjectId] = None,
        created_at: Optional[datetime] = None,
    ):
        self._id = _id or ObjectId()
        self.title = title
        self.genre = genre
        self.year = year
        self.rating = rating
        self.description = description
        self.poster_url = poster_url
        self.trailer_url = trailer_url
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "title": self.title,
            "genre": self.genre,
            "year": self.year,
            "rating": self.rating,
            "description": self.description,
            "poster_url": self.poster_url,
            "trailer_url": self.trailer_url,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "Movie":
        return Movie(
            title=data.get("title"),
            genre=data.get("genre", []),
            year=data.get("year"),
            rating=data.get("rating"),
            description=data.get("description"),
            poster_url=data.get("poster_url"),
            trailer_url=data.get("trailer_url"),
            _id=data.get("_id"),
            created_at=data.get("created_at"),
        )
