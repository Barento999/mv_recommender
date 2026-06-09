#!/usr/bin/env python3
"""Test to verify recommendations are being returned."""

import sys
sys.path.insert(0, '/home/barento/Desktop/reco/backend')

import asyncio
from bson import ObjectId
from app.database import connect_to_mongo, close_mongo_connection, get_database
from app.services.recommendation_service import get_recommendations

async def test_recommendations():
    await connect_to_mongo()
    db = get_database()
    
    print("🧪 Testing Recommendations System\n")
    print("=" * 70)
    
    # Get a test user
    user = await db.users.find_one()
    if not user:
        print("❌ No users found in database")
        await close_mongo_connection()
        return
    
    user_id = str(user["_id"])
    user_name = user.get("name", "Unknown")
    
    print(f"\n1️⃣ Testing with user: {user_name} ({user_id})")
    print("-" * 70)
    
    # Check user's activity
    favorites = await db.favorites.find({"user_id": user["_id"]}).to_list(None)
    ratings = await db.ratings.find({"user_id": user["_id"]}).to_list(None)
    
    print(f"   Favorites: {len(favorites)}")
    print(f"   Ratings: {len(ratings)}")
    
    # Get recommendations
    print(f"\n2️⃣ Getting recommendations...")
    print("-" * 70)
    
    recommendations = await get_recommendations(user_id, limit=10)
    
    print(f"✅ Got {len(recommendations)} recommendations\n")
    
    if recommendations:
        print(f"Recommendations:")
        for i, movie in enumerate(recommendations[:5], 1):
            print(f"   {i}. {movie.title} ({movie.year})")
            print(f"      Rating: {movie.rating}/10")
            print(f"      Genres: {', '.join(movie.genre[:2])}")
    else:
        print("⚠️  No recommendations returned")
    
    print("\n" + "=" * 70)
    
    await close_mongo_connection()

asyncio.run(test_recommendations())
