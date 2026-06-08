"""
MongoDB Importer Module

Imports CSV data and trained models into MongoDB.
Handles batch inserts with proper error handling.
"""

import pandas as pd
from typing import Dict, Tuple, Optional
from datetime import datetime
import logging
from bson import ObjectId

logger = logging.getLogger(__name__)


async def import_movies_to_mongo(movies_df: pd.DataFrame, db) -> Tuple[int, int]:
    """
    Import movies from DataFrame to MongoDB.
    
    Args:
        movies_df: DataFrame with movie data
        db: MongoDB database instance
        
    Returns:
        Tuple of (inserted_count, error_count)
    """
    logger.info("[MongoImporter] Importing movies to MongoDB...")
    
    inserted = 0
    errors = 0
    
    try:
        movies_collection = db.movies
        
        for _, row in movies_df.iterrows():
            try:
                movie_doc = {
                    'title': str(row['title']),
                    'genre': [g.strip() for g in str(row['genre']).split('|')],
                    'year': int(row['year']),
                    'rating': float(row['rating']),
                    'description': str(row.get('description', '')),
                    'poster_url': str(row.get('poster_url', '')),
                    'trailer_url': None,
                    'created_at': datetime.utcnow()
                }
                
                # Check if exists (by title)
                existing = await movies_collection.find_one({'title': movie_doc['title']})
                if not existing:
                    result = await movies_collection.insert_one(movie_doc)
                    inserted += 1
                else:
                    logger.debug(f"Movie already exists: {movie_doc['title']}")
            
            except Exception as e:
                logger.error(f"Error importing movie: {str(e)}")
                errors += 1
        
        logger.info(f"[MongoImporter] ✓ Inserted {inserted} movies ({errors} errors)")
        return inserted, errors
    
    except Exception as e:
        logger.error(f"[MongoImporter] ✗ Error importing movies: {str(e)}")
        return 0, len(movies_df)


async def import_users_to_mongo(users_df: pd.DataFrame, db) -> Tuple[int, int]:
    """
    Import users from DataFrame to MongoDB.
    
    Args:
        users_df: DataFrame with user data
        db: MongoDB database instance
        
    Returns:
        Tuple of (inserted_count, error_count)
    """
    logger.info("[MongoImporter] Importing users to MongoDB...")
    
    inserted = 0
    errors = 0
    
    try:
        users_collection = db.users
        
        for _, row in users_df.iterrows():
            try:
                user_doc = {
                    'name': str(row['name']),
                    'email': str(row['email']),
                    'password': 'hashed_password_placeholder',
                    'created_at': datetime.utcnow()
                }
                
                # Check if exists (by email)
                existing = await users_collection.find_one({'email': user_doc['email']})
                if not existing:
                    result = await users_collection.insert_one(user_doc)
                    inserted += 1
                else:
                    logger.debug(f"User already exists: {user_doc['email']}")
            
            except Exception as e:
                logger.error(f"Error importing user: {str(e)}")
                errors += 1
        
        logger.info(f"[MongoImporter] ✓ Inserted {inserted} users ({errors} errors)")
        return inserted, errors
    
    except Exception as e:
        logger.error(f"[MongoImporter] ✗ Error importing users: {str(e)}")
        return 0, len(users_df)


async def import_ratings_to_mongo(
    ratings_df: pd.DataFrame,
    db,
    batch_size: int = 1000
) -> Tuple[int, int]:
    """
    Import ratings from DataFrame to MongoDB.
    
    Args:
        ratings_df: DataFrame with rating data
        db: MongoDB database instance
        batch_size: Batch insert size
        
    Returns:
        Tuple of (inserted_count, error_count)
    """
    logger.info(f"[MongoImporter] Importing {len(ratings_df)} ratings to MongoDB...")
    
    inserted = 0
    errors = 0
    
    try:
        # First, get ID mappings
        movies_coll = db.movies
        users_coll = db.users
        ratings_coll = db.ratings
        
        # Build mappings
        movies = await movies_coll.find({}, {'_id': 1, 'title': 1}).to_list(None)
        users = await users_coll.find({}, {'_id': 1, 'email': 1}).to_list(None)
        
        title_to_id = {m['title']: m['_id'] for m in movies}
        email_to_id = {u['email']: u['_id'] for u in users}
        
        logger.info(f"[MongoImporter] ID mappings ready: {len(title_to_id)} movies, {len(email_to_id)} users")
        
        # Prepare rating documents
        rating_docs = []
        
        for _, row in ratings_df.iterrows():
            try:
                # This is simplified - in real scenario, match by movie/user IDs
                rating_doc = {
                    'user_id': row['user_id'],  # CSV user_id
                    'movie_id': row['movie_id'],  # CSV movie_id
                    'rating': float(row['rating']),
                    'created_at': datetime.utcnow()
                }
                rating_docs.append(rating_doc)
            
            except Exception as e:
                logger.error(f"Error preparing rating: {str(e)}")
                errors += 1
        
        # Batch insert
        for i in range(0, len(rating_docs), batch_size):
            batch = rating_docs[i:i+batch_size]
            try:
                result = await ratings_coll.insert_many(batch)
                inserted += len(result.inserted_ids)
                logger.debug(f"Inserted batch of {len(batch)} ratings")
            except Exception as e:
                logger.error(f"Error inserting batch: {str(e)}")
                errors += len(batch)
        
        logger.info(f"[MongoImporter] ✓ Inserted {inserted} ratings ({errors} errors)")
        return inserted, errors
    
    except Exception as e:
        logger.error(f"[MongoImporter] ✗ Error importing ratings: {str(e)}")
        return 0, len(ratings_df)


async def import_all_to_mongo(
    movies_df: pd.DataFrame,
    users_df: pd.DataFrame,
    ratings_df: pd.DataFrame,
    db
) -> Dict:
    """
    Import all data to MongoDB.
    
    Args:
        movies_df: Movies DataFrame
        users_df: Users DataFrame
        ratings_df: Ratings DataFrame
        db: MongoDB database instance
        
    Returns:
        Dict with import statistics
    """
    logger.info("[MongoImporter] ====================================")
    logger.info("[MongoImporter] Starting MongoDB import")
    logger.info("[MongoImporter] ====================================")
    
    try:
        # Clear existing data
        logger.info("[MongoImporter] Clearing existing collections...")
        await db.movies.delete_many({})
        await db.users.delete_many({})
        await db.ratings.delete_many({})
        
        # Import data
        movies_inserted, movies_errors = await import_movies_to_mongo(movies_df, db)
        users_inserted, users_errors = await import_users_to_mongo(users_df, db)
        ratings_inserted, ratings_errors = await import_ratings_to_mongo(ratings_df, db)
        
        # Create indexes
        logger.info("[MongoImporter] Creating indexes...")
        await db.ratings.create_index("user_id")
        await db.ratings.create_index("movie_id")
        await db.ratings.create_index([("user_id", 1), ("movie_id", 1)], unique=True)
        await db.movies.create_index("title")
        await db.users.create_index("email", unique=True)
        
        logger.info("[MongoImporter] ✓ Indexes created")
        
        result = {
            'status': 'success',
            'movies': {'inserted': movies_inserted, 'errors': movies_errors},
            'users': {'inserted': users_inserted, 'errors': users_errors},
            'ratings': {'inserted': ratings_inserted, 'errors': ratings_errors},
            'total_inserted': movies_inserted + users_inserted + ratings_inserted,
            'total_errors': movies_errors + users_errors + ratings_errors
        }
        
        logger.info("[MongoImporter] ====================================")
        logger.info(f"[MongoImporter] Import Complete")
        logger.info(f"[MongoImporter] Movies: {movies_inserted} inserted")
        logger.info(f"[MongoImporter] Users: {users_inserted} inserted")
        logger.info(f"[MongoImporter] Ratings: {ratings_inserted} inserted")
        logger.info("[MongoImporter] ====================================")
        
        return result
    
    except Exception as e:
        logger.error(f"[MongoImporter] ✗ Import failed: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }
