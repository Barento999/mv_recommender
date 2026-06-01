from pydantic import BaseModel, Field
from typing import List
from .movie import MovieResponse

class RecommendationResponse(BaseModel):
    recommendations: List[MovieResponse]
    count: int
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "recommendations": [],
                "count": 0,
                "message": "Recommendations based on your favorites",
            }
        }
