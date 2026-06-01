import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.models.movie import Movie

sample_movies = [
    Movie(
        title="The Shawshank Redemption",
        genre=["Drama"],
        year=1994,
        rating=9.3,
        description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        poster_url="https://images.unsplash.com/photo-1516738901601-de13f8df52ef?w=400&h=600&fit=crop",
        trailer_url="https://www.youtube.com/embed/6_nFI2Zb7qE",
    ),
    Movie(
        title="The Dark Knight",
        genre=["Action", "Crime", "Drama"],
        year=2008,
        rating=9.0,
        description="When the menace known as the Joker wreaks havoc and chaos on Gotham, Batman must accept one of psychology and morality's greatest tests.",
        poster_url="https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=600&fit=crop",
        trailer_url="https://www.youtube.com/embed/EXeTwQWrcwY",
    ),
    Movie(
        title="Inception",
        genre=["Action", "Sci-Fi", "Thriller"],
        year=2010,
        rating=8.8,
        description="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.",
        poster_url="https://images.unsplash.com/photo-1485846234645-a62644f84728?w=400&h=600&fit=crop",
        trailer_url="https://www.youtube.com/embed/YoHD_XwIlNY",
    ),
    Movie(
        title="Pulp Fiction",
        genre=["Crime", "Drama"],
        year=1994,
        rating=8.9,
        description="The lives of two mob hitmen, a boxer, a gangster's wife and a pair of diner bandits intertwine in four tales of violence and redemption.",
        poster_url="https://images.unsplash.com/photo-1515612141207-8a88fb8ce338?w=400&h=600&fit=crop",
        trailer_url="https://www.youtube.com/embed/tHRH4lT9nqE",
    ),
    Movie(
        title="Forrest Gump",
        genre=["Drama", "Romance"],
        year=1994,
        rating=8.8,
        description="The presidencies of Kennedy and Johnson unfold from the perspective of an Alabama man with an IQ of 75.",
        poster_url="https://images.unsplash.com/photo-1533613220915-609f71a91335?w=400&h=600&fit=crop",
        trailer_url="https://www.youtube.com/embed/bLvqoByEnEE",
    ),
    Movie(
        title="Interstellar",
        genre=["Adventure", "Drama", "Sci-Fi"],
        year=2014,
        rating=8.7,
        description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        poster_url="https://images.unsplash.com/photo-1489599849228-2e604dec712e?w=400&h=600&fit=crop",
        trailer_url="https://www.youtube.com/embed/0vOM9yJJt-E",
    ),
]

async def seed_movies():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]

    try:
        # Clear existing movies
        await db.movies.delete_many({})
        print("✓ Cleared existing movies")

        # Insert sample movies
        movies_data = [m.to_dict() for m in sample_movies]
        result = await db.movies.insert_many(movies_data)
        print(f"✓ Inserted {len(result.inserted_ids)} sample movies")

    except Exception as e:
        print(f"✗ Error seeding movies: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_movies())
