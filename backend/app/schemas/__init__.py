from .user import UserRegister, UserLogin, UserResponse
from .movie import MovieCreate, MovieUpdate, MovieResponse
from .rating import RatingCreate, RatingResponse
from .favorite import FavoriteResponse
from .recommendation import RecommendationResponse

__all__ = [
    "UserRegister",
    "UserLogin",
    "UserResponse",
    "MovieCreate",
    "MovieUpdate",
    "MovieResponse",
    "RatingCreate",
    "RatingResponse",
    "FavoriteResponse",
    "RecommendationResponse",
]
