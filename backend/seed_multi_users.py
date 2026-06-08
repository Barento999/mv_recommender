"""
Seed multiple users with ratings for ML model training
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.models.user import User
from app.models.rating import Rating
from app.utils.security import hash_password
from bson import ObjectId

async def seed_multi_user_ratings():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]

    try:
        # Get all movies
        movies = await db.movies.find({}).to_list(None)
        if not movies:
            print("No movies found")
            return

        # Create test users with different preferences
        test_users = [
            {
                "email": "user2@example.com",
                "name": "Action Lover",
                "ratings": [
                    (0, 4.0),  # Shawshank - Drama
                    (1, 5.0),  # Dark Knight - Action/Crime
                    (2, 5.0),  # Inception - Action/Sci-Fi
                    (3, 3.5),  # Pulp Fiction - Crime/Drama
                    (4, 2.0),  # Forrest Gump - Drama/Romance
                    (5, 4.5),  # Interstellar - Adventure/Sci-Fi
                ]
            },
            {
                "email": "user3@example.com",
                "name": "Drama Fan",
                "ratings": [
                    (0, 5.0),  # Shawshank - Drama
                    (1, 3.5),  # Dark Knight - Action
                    (2, 3.0),  # Inception - Sci-Fi
                    (3, 4.5),  # Pulp Fiction - Drama
                    (4, 5.0),  # Forrest Gump - Drama/Romance
                    (5, 3.0),  # Interstellar - Adventure
                ]
            },
            {
                "email": "user4@example.com",
                "name": "Sci-Fi Enthusiast",
                "ratings": [
                    (0, 3.0),  # Shawshank - Drama
                    (1, 4.0),  # Dark Knight - Action
                    (2, 5.0),  # Inception - Sci-Fi
                    (3, 2.5),  # Pulp Fiction - Crime
                    (4, 3.0),  # Forrest Gump - Drama
                    (5, 5.0),  # Interstellar - Sci-Fi/Adventure
                ]
            },
        ]

        for user_data in test_users:
            # Check if user exists
            existing = await db.users.find_one({"email": user_data["email"]})
            if existing:
                user_id = existing["_id"]
                print(f"User {user_data['email']} already exists")
            else:
                # Create new user
                user = User(
                    name=user_data["name"],
                    email=user_data["email"],
                    password=hash_password("password123")
                )
                result = await db.users.insert_one(user.to_dict())
                user_id = result.inserted_id
                print(f"✓ Created user: {user_data['name']} ({user_data['email']})")

            # Clear existing ratings for this user
            await db.ratings.delete_many({"user_id": user_id})

            # Add ratings
            for movie_idx, rating_value in user_data["ratings"]:
                rating = Rating(
                    user_id=user_id,
                    movie_id=movies[movie_idx]["_id"],
                    rating=rating_value
                )
                await db.ratings.insert_one(rating.to_dict())
            
            print(f"  ✓ Added {len(user_data['ratings'])} ratings")

        print(f"\n✓ Seeded {len(test_users)} test users with ratings")
        
        # Verify total ratings
        total_ratings = await db.ratings.count_documents({})
        print(f"✓ Total ratings in database: {total_ratings}")

    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_multi_user_ratings())
