"""
Reseed database with updated movie data
"""

import asyncio
from app.database import get_database, connect_to_mongo, close_mongo_connection
from app.services.seed_service import seed_database

async def reseed():
    await connect_to_mongo()
    
    db = get_database()
    
    # Clear existing data
    print("Clearing existing data...")
    await db.movies.delete_many({})
    await db.users.delete_many({})
    await db.ratings.delete_many({})
    print("✅ Cleared collections")
    
    # Reseed
    print("\nReseeding database...")
    success = await seed_database()
    
    if success:
        # Verify
        movie_count = await db.movies.count_documents({})
        user_count = await db.users.count_documents({})
        rating_count = await db.ratings.count_documents({})
        
        print(f"\n✅ Database reseeded successfully!")
        print(f"   Movies: {movie_count}")
        print(f"   Users: {user_count}")
        print(f"   Ratings: {rating_count}")
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(reseed())
