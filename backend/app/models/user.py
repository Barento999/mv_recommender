from datetime import datetime
from typing import Optional
from bson import ObjectId

class User:
    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        _id: Optional[ObjectId] = None,
        created_at: Optional[datetime] = None,
    ):
        self._id = _id or ObjectId()
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "User":
        return User(
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
            _id=data.get("_id"),
            created_at=data.get("created_at"),
        )
