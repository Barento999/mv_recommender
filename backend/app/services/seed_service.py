"""
Automatic Data Seeding Service
Loads CSV data into MongoDB on app startup
"""

import logging
import pandas as pd
from pathlib import Path
from app.database import get_database
from bson import ObjectId
from datetime import datetime
from app.middleware.rbac import get_permission_list

logger = logging.getLogger(__name__)


async def seed_database():
    """
    Automatically seed database with CSV data on app startup.
    
    Loads:
    - 2,000 movies from data/movies.csv
    - 150 users from data/users.csv
    - 14,725 ratings from data/ratings.csv
    - 1 admin user for testing
    """
    
    db = get_database()
    
    try:
        # Check if data already seeded
        movie_count = await db.movies.count_documents({})
        
        if movie_count > 0:
            logger.info(f"✅ Database already seeded with {movie_count} movies")
            # Still check for admin user
            await seed_admin_user(db)
            return True
        
        logger.info("\n" + "="*70)
        logger.info("📊 SEEDING DATABASE FROM CSV")
        logger.info("="*70)
        
        # Load CSV files
        data_dir = Path(__file__).parent.parent.parent / "data"
        
        # Seed Movies
        logger.info("\n[1/3] Loading movies...")
        movies_df = pd.read_csv(data_dir / "movies.csv")
        
        movies_data = []
        for _, row in movies_df.iterrows():
            movie = {
                "_id": ObjectId(),
                "movie_id": row.get("movie_id", ""),
                "title": row.get("title", ""),
                "genre": [g.strip() for g in str(row.get("genre", "")).split("|")] if pd.notna(row.get("genre")) else [],
                "year": int(row.get("year", 0)) if pd.notna(row.get("year")) else 0,
                "rating": float(row.get("rating", 0)) if pd.notna(row.get("rating")) else 0.0,
                "description": row.get("description", ""),
                "poster_url": row.get("poster_url", ""),
                "trailer_url": row.get("trailer_url", ""),
                "created_at": datetime.utcnow(),
            }
            movies_data.append(movie)
        
        if movies_data:
            await db.movies.insert_many(movies_data)
            logger.info(f"✅ Seeded {len(movies_data)} movies")
        
        # Seed Users
        logger.info("\n[2/3] Loading users...")
        users_df = pd.read_csv(data_dir / "users.csv")
        
        users_data = []
        for _, row in users_df.iterrows():
            user = {
                "_id": ObjectId(),
                "user_id": row.get("user_id", ""),
                "name": row.get("name", ""),
                "email": row.get("email", ""),
                "role": "user",
                "permissions": get_permission_list("user"),
                "created_at": datetime.utcnow(),
            }
            users_data.append(user)
        
        if users_data:
            await db.users.insert_many(users_data)
            logger.info(f"✅ Seeded {len(users_data)} users")
        
        # Seed Ratings
        logger.info("\n[3/3] Loading ratings...")
        ratings_df = pd.read_csv(data_dir / "ratings.csv")
        
        ratings_data = []
        for _, row in ratings_df.iterrows():
            rating = {
                "_id": ObjectId(),
                "user_id": row.get("user_id", ""),
                "movie_id": row.get("movie_id", ""),
                "rating": float(row.get("rating", 0)) if pd.notna(row.get("rating")) else 0.0,
                "created_at": datetime.utcnow(),
            }
            ratings_data.append(rating)
        
        if ratings_data:
            await db.ratings.insert_many(ratings_data)
            logger.info(f"✅ Seeded {len(ratings_data)} ratings")
        
        # Seed admin user
        await seed_admin_user(db)
        
        logger.info("\n" + "="*70)
        logger.info("✅ DATABASE SEEDING COMPLETE")
        logger.info("="*70)
        logger.info(f"\nData Summary:")
        logger.info(f"  Movies: {len(movies_data)}")
        logger.info(f"  Users: {len(users_data)}")
        logger.info(f"  Ratings: {len(ratings_data)}")
        logger.info("="*70 + "\n")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error seeding database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def seed_admin_user(db):
    """Create a default admin user for testing if it doesn't exist."""
    try:
        # Check if admin already exists
        admin_exists = await db.users.find_one({"email": "admin@movierego.com"})
        
        if admin_exists:
            logger.info("✅ Admin user already exists")
            return
        
        # Create admin user (password will be handled by auth routes)
        admin_user = {
            "_id": ObjectId(),
            "name": "Admin User",
            "email": "admin@movierego.com",
            "password_hash": "",  # Will be set during registration/manual setup
            "role": "admin",
            "permissions": get_permission_list("admin"),
            "created_at": datetime.utcnow(),
        }
        
        result = await db.users.insert_one(admin_user)
        logger.info(f"✅ Created admin user (ID: {result.inserted_id})")
        logger.info("\n📌 ADMIN CREDENTIALS FOR TESTING:")
        logger.info("   Email: admin@movierego.com")
        logger.info("   Password: (Set via registration or manual setup)")
        logger.info("   Note: Use the registration page or update password manually\n")
        
    except Exception as e:
        logger.error(f"Error seeding admin user: {str(e)}")

