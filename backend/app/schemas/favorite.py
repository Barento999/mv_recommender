from pydantic import BaseModel, Field
from datetime import datetime

class FavoriteResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    movie_id: str
    created_at: datetime

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439012",
                "user_id": "507f1f77bcf86cd799439010",
                "movie_id": "507f1f77bcf86cd799439011",
                "created_at": "2024-01-01T12:00:00",
            }
        }
