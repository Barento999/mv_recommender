from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional, List
from app.schemas.movie import MovieCreate, MovieUpdate, MovieResponse
from app.services.movie_service import (
    create_movie,
    get_movie_by_id,
    get_all_movies,
    search_movies,
    filter_movies_by_rating,
    update_movie,
    delete_movie,
)
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/movies", tags=["movies"])

@router.post("", response_model=MovieResponse)
async def create_new_movie(
    movie_data: MovieCreate,
    current_user: User = Depends(get_current_user),
):
    movie = await create_movie(
        title=movie_data.title,
        genre=movie_data.genre,
        year=movie_data.year,
        rating=movie_data.rating,
        description=movie_data.description,
        poster_url=movie_data.poster_url,
        trailer_url=movie_data.trailer_url,
    )
    return {
        "_id": str(movie._id),
        "title": movie.title,
        "genre": movie.genre,
        "year": movie.year,
        "rating": movie.rating,
        "description": movie.description,
        "poster_url": movie.poster_url,
        "trailer_url": movie.trailer_url,
        "created_at": movie.created_at,
    }

@router.get("", response_model=dict)
async def list_movies(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    genre: Optional[str] = None,
    year: Optional[int] = None,
    min_rating: Optional[float] = Query(None, ge=0, le=10),
):
    if min_rating:
        movies, total = await filter_movies_by_rating(min_rating, skip, limit)
    else:
        movies, total = await get_all_movies(skip, limit, genre, year)

    return {
        "movies": [
            {
                "_id": str(m._id),
                "title": m.title,
                "genre": m.genre,
                "year": m.year,
                "rating": m.rating,
                "description": m.description,
                "poster_url": m.poster_url,
                "trailer_url": m.trailer_url,
                "created_at": m.created_at,
            }
            for m in movies
        ],
        "total": total,
        "skip": skip,
        "limit": limit,
    }

@router.get("/search", response_model=dict)
async def search(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    movies, total = await search_movies(q, skip, limit)
    return {
        "movies": [
            {
                "_id": str(m._id),
                "title": m.title,
                "genre": m.genre,
                "year": m.year,
                "rating": m.rating,
                "description": m.description,
                "poster_url": m.poster_url,
                "trailer_url": m.trailer_url,
                "created_at": m.created_at,
            }
            for m in movies
        ],
        "total": total,
        "query": q,
    }

@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: str):
    movie = await get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    return {
        "_id": str(movie._id),
        "title": movie.title,
        "genre": movie.genre,
        "year": movie.year,
        "rating": movie.rating,
        "description": movie.description,
        "poster_url": movie.poster_url,
        "trailer_url": movie.trailer_url,
        "created_at": movie.created_at,
    }

@router.put("/{movie_id}", response_model=MovieResponse)
async def update_movie_route(
    movie_id: str,
    movie_data: MovieUpdate,
    current_user: User = Depends(get_current_user),
):
    update_dict = movie_data.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data to update")

    movie = await update_movie(movie_id, update_dict)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    return {
        "_id": str(movie._id),
        "title": movie.title,
        "genre": movie.genre,
        "year": movie.year,
        "rating": movie.rating,
        "description": movie.description,
        "poster_url": movie.poster_url,
        "trailer_url": movie.trailer_url,
        "created_at": movie.created_at,
    }

@router.delete("/{movie_id}")
async def delete_movie_route(
    movie_id: str,
    current_user: User = Depends(get_current_user),
):
    success = await delete_movie(movie_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    return {"message": "Movie deleted successfully"}
