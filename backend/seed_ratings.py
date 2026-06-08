"""
Seed ratings data for testing ML recommendations
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.models.rating import Rating
from bson import ObjectId

async def seed_ratings():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]

    try:
        # Get the test user
        user = await db.users.find_one({"email": "testuser@example.com"})
        if not user:
            print("Test user not found")
            return

        user_id = user["_id"]

        # Get all movies
        movies = await db.movies.find({}).to_list(None)
        if not movies:
            print("No movies found")
            return

        # Clear existing ratings for this user
        await db.ratings.delete_many({"user_id": user_id})
        print("✓ Cleared existing ratings")

        # Create ratings: user likes drama and action, loves The Shawshank Redemption
        ratings_data = [
            {"movie_id": movies[0]["_id"], "rating": 5.0},  # The Shawshank Redemption - Drama
            {"movie_id": movies[1]["_id"], "rating": 4.5},  # The Dark Knight - Action/Crime
            {"movie_id": movies[2]["_id"], "rating": 4.0},  # Inception - Action/Sci-Fi
            {"movie_id": movies[3]["_id"], "rating": 3.5},  # Pulp Fiction - Crime/Drama
            {"movie_id": movies[4]["_id"], "rating": 4.5},  # Forrest Gump - Drama/Romance
        ]

        inserted_ratings = []
        for rating_data in ratings_data:
            rating = Rating(
                user_id=user_id,
                movie_id=rating_data["movie_id"],
                rating=rating_data["rating"]
            )
            result = await db.ratings.insert_one(rating.to_dict())
            inserted_ratings.append(result.inserted_id)
            print(f"  ✓ Added rating: {rating.rating}★ for movie {rating.movie_id}")

        print(f"✓ Added {len(inserted_ratings)} ratings for testing")

    except Exception as e:
        print(f"✗ Error seeding ratings: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_ratings())
