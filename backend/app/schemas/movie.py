from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import List, Optional

class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    genre: List[str] = Field(..., min_items=1)
    year: int = Field(..., ge=1800, le=2100)
    rating: float = Field(..., ge=0, le=10)
    description: str = Field(..., min_length=10)
    poster_url: str
    trailer_url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Shawshank Redemption",
                "genre": ["Drama", "Crime"],
                "year": 1994,
                "rating": 9.3,
                "description": "Two imprisoned men bond...",
                "poster_url": "https://example.com/poster.jpg",
                "trailer_url": "https://youtube.com/watch?v=...",
            }
        }

class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    genre: Optional[List[str]] = Field(None, min_items=1)
    year: Optional[int] = Field(None, ge=1800, le=2100)
    rating: Optional[float] = Field(None, ge=0, le=10)
    description: Optional[str] = Field(None, min_length=10)
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None

class MovieResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    genre: List[str]
    year: int
    rating: float
    description: str
    poster_url: str
    trailer_url: Optional[str] = None
    created_at: datetime

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "title": "The Shawshank Redemption",
                "genre": ["Drama", "Crime"],
                "year": 1994,
                "rating": 9.3,
                "description": "Two imprisoned men bond...",
                "poster_url": "https://example.com/poster.jpg",
                "trailer_url": "https://youtube.com/watch?v=...",
                "created_at": "2024-01-01T12:00:00",
            }
        }
