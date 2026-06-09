from fastapi import Depends, APIRouter, Query
from app.database import get_database
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/search/advanced")
async def advanced_search(
    query: Optional[str] = Query(None, min_length=0, max_length=100),
    genres: Optional[str] = Query(None, description="Comma-separated genres"),
    min_rating: float = Query(0, ge=0, le=10),
    max_rating: float = Query(10, ge=0, le=10),
    min_year: int = Query(1900, ge=1900, le=2026),
    max_year: int = Query(2026, ge=1900, le=2026),
    sort_by: str = Query("rating", regex="^(rating|year|title)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """
    Advanced movie search with filtering and sorting.
    
    Parameters:
    - query: Search in title and description
    - genres: Comma-separated genre names (e.g., "Action,Sci-Fi")
    - min_rating/max_rating: Rating range (0-10)
    - min_year/max_year: Release year range
    - sort_by: Sort by 'rating', 'year', or 'title'
    - sort_order: 'asc' for ascending, 'desc' for descending
    - skip/limit: Pagination
    """
    try:
        # Build filter query
        filter_query = {}
        
        # Text search
        if query and query.strip():
            search_query = query.strip()
            filter_query["$or"] = [
                {"title": {"$regex": search_query, "$options": "i"}},
                {"description": {"$regex": search_query, "$options": "i"}}
            ]
        
        # Genre filter
        if genres and genres.strip():
            genre_list = [g.strip() for g in genres.split(",") if g.strip()]
            if genre_list:
                filter_query["genre"] = {"$in": genre_list}
        
        # Rating filter
        rating_filter = {}
        if min_rating > 0:
            rating_filter["$gte"] = min_rating
        if max_rating < 10:
            rating_filter["$lte"] = max_rating
        if rating_filter:
            filter_query["rating"] = rating_filter
        
        # Year filter
        year_filter = {}
        if min_year > 1900:
            year_filter["$gte"] = min_year
        if max_year < 2026:
            year_filter["$lte"] = max_year
        if year_filter:
            filter_query["year"] = year_filter
        
        # Build sort order
        sort_direction = -1 if sort_order == "desc" else 1
        sort_key = "rating" if sort_by == "rating" else ("year" if sort_by == "year" else "title")
        
        # Execute query
        movies_collection = db.movies
        
        # Get total count
        total_count = await movies_collection.count_documents(filter_query)
        
        # Get paginated results
        movies = await movies_collection.find(filter_query).sort(sort_key, sort_direction).skip(skip).limit(limit).to_list(None)
        
        # Format response
        return {
            "movies": [
                {
                    "_id": str(m["_id"]),
                    "title": m.get("title", "Unknown"),
                    "genre": m.get("genre", []),
                    "year": m.get("year", 0),
                    "rating": m.get("rating", 0),
                    "description": m.get("description", ""),
                    "poster_url": m.get("poster_url", ""),
                    "trailer_url": m.get("trailer_url", ""),
                }
                for m in movies
            ],
            "total": total_count,
            "count": len(movies),
            "skip": skip,
            "limit": limit,
            "page": skip // limit + 1 if limit > 0 else 1,
            "total_pages": (total_count + limit - 1) // limit if limit > 0 else 1
        }
        
    except Exception as e:
        logger.error(f"Error in advanced search: {str(e)}")
        return {
            "movies": [],
            "total": 0,
            "count": 0,
            "skip": skip,
            "limit": limit,
            "error": str(e)
        }


@router.get("/filters/metadata")
async def get_filter_metadata(
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get metadata for advanced filtering (genres, year range, rating range)."""
    try:
        movies_collection = db.movies
        
        # Get unique genres
        genres = await movies_collection.distinct("genre")
        genres = sorted([g for g in genres if g])
        
        # Get year range
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "min_year": {"$min": "$year"},
                    "max_year": {"$max": "$year"},
                    "min_rating": {"$min": "$rating"},
                    "max_rating": {"$max": "$rating"}
                }
            }
        ]
        
        result = await movies_collection.aggregate(pipeline).to_list(None)
        
        if result:
            data = result[0]
            return {
                "genres": genres,
                "year_range": {
                    "min": int(data.get("min_year", 1900)),
                    "max": int(data.get("max_year", 2026))
                },
                "rating_range": {
                    "min": float(data.get("min_rating", 0)),
                    "max": float(data.get("max_rating", 10))
                },
                "genre_count": len(genres)
            }
        
        return {
            "genres": [],
            "year_range": {"min": 1900, "max": 2026},
            "rating_range": {"min": 0, "max": 10},
            "genre_count": 0
        }
        
    except Exception as e:
        logger.error(f"Error getting filter metadata: {str(e)}")
        return {
            "genres": [],
            "year_range": {"min": 1900, "max": 2026},
            "rating_range": {"min": 0, "max": 10},
            "genre_count": 0,
            "error": str(e)
        }
