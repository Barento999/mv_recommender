"""
Comprehensive Data Seeding Script: 2000 Movies + Realistic Ratings

This script generates:
- 2000 diverse movies with realistic metadata (title, genre, year, description, rating)
- 150 users
- ~8,000-12,000 ratings distributed realistically across users

The goal is to create enough data for the collaborative filtering model to:
1. Build a meaningful user-item matrix
2. Compute user-user similarities
3. Generate quality personalized recommendations

Data Distribution:
- Movie genres: 15+ genres with realistic category overlap
- Release years: 1970-2024
- User behavior: Heavy-tail distribution (some users rate many movies, most rate fewer)
- Rating distribution: Skewed toward positive ratings (realistic user bias)
"""

import asyncio
import random
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
import motor.motor_asyncio as motor


# ============================================================================
# DATA CONSTANTS
# ============================================================================

GENRES = [
    "Action", "Comedy", "Drama", "Horror", "Thriller", "Sci-Fi", "Fantasy",
    "Romance", "Animation", "Adventure", "Crime", "Documentary", "Family",
    "History", "Mystery", "Western", "War", "Sport", "Musical", "Biography"
]

MOVIE_TITLES = [
    # Action
    "Velocity Vortex", "Shadow Protocol", "Midnight Strike", "Quantum Breach",
    "Phoenix Rising", "Silent Reckoning", "Chaos Theory", "Iron Guardian",
    "Lethal Alliance", "Fortress Unbreakable", "Thunder Down", "Apex Predator",
    
    # Drama
    "Echoes of Tomorrow", "Fractured Dreams", "Crossroads Destiny", "Silent Witness",
    "Breaking Point", "The Last Goodbye", "Redemption Road", "Unraveled Hearts",
    "The Weight of Years", "Forgotten Souls", "Shattered Reflections", "Beneath the Surface",
    
    # Comedy
    "Laughing Matter", "Chaos Control", "Blissful Chaos", "Perfect Timing",
    "The Awkward Truth", "Love's Misfortune", "Dating Disasters", "Friends Forever",
    "Weekend Getaway", "Office Legends", "Road Trip Chronicles", "Wedding Bells",
    
    # Sci-Fi
    "Neural Nexus", "Temporal Shift", "The Last Horizon", "Digital Dreams",
    "Void Explorer", "Infinite Loop", "Cosmic Collision", "Future Wars",
    "Time Paradox", "Cyber Awakening", "The Singularity Event", "Dimensional Breach",
    
    # Horror
    "Midnight Terror", "The Haunting", "Crimson Shadows", "Fear Manifest",
    "The Descent", "Nightmare Realm", "Curse of the Forgotten", "The Awakening",
    "Darkness Calls", "The Reckoning", "Possessed", "Final Scream",
    
    # Romance
    "A Second Chance", "Hearts Collide", "Love Beyond Time", "Sunset Promise",
    "The One That Got Away", "Forever Tonight", "Destiny Awaits", "Love Unbound",
    "Against the Odds", "Beneath the Stars", "First Light", "Eternal Flame",
    
    # Fantasy
    "Dragon's Legacy", "The Forbidden Crown", "Quest for Magic", "Realm Eternal",
    "The Last Sorcerer", "Knights of Old", "Enchanted Land", "The prophecy Fulfilled",
    "Wizard's Tower", "The Shadowlands", "Rise of the Chosen", "Gateway to Wonder",
    
    # Thriller
    "The Conspiracy", "Breaking Cover", "The Hunt Begins", "Deadly Deception",
    "Hunt or Be Hunted", "The Setup", "Betrayal's Edge", "No Escape",
    "The Final Game", "Twisted Truth", "The Snare", "Last Stand",
    
    # Animation
    "Pixel Dreams", "The Journey Home", "Quest for Stars", "Adventures Await",
    "Colors of Joy", "Magical Forest", "Beyond the Rainbow", "Heroes Rise",
    "The Last Guardian", "Spirit Realm", "Mystic Tales", "Wonder Quest",
    
    # Adventure
    "Jungle Expedition", "The Lost City", "Mountain Peak", "Desert Crossing",
    "Ocean Depths", "Arctic Expedition", "Treasure Hunt", "Into the Unknown",
    "Path of Discovery", "Great Escape", "Paradise Found", "The Grand Journey",
]

DESCRIPTIONS_TEMPLATES = [
    "An epic tale of {genre.lower()} following {protagonist} as they face their greatest challenge yet.",
    "When {protagonist} discovers a life-changing secret, everything falls apart in this gripping {genre.lower()}.",
    "A thrilling {genre.lower()} about {protagonist}'s quest for {goal}.",
    "In this powerful {genre.lower()}, {protagonist} must overcome impossible odds to {goal}.",
    "A compelling story about {protagonist} learning to {goal} in this {genre.lower()} masterpiece.",
    "When darkness falls, only {protagonist} can save the day in this intense {genre.lower()}.",
    "Follow {protagonist}'s incredible journey in this unforgettable {genre.lower()}.",
    "A {genre.lower()} that explores the depths of human emotion through {protagonist}'s eyes.",
    "An action-packed {genre.lower()} featuring {protagonist} against all odds.",
    "This stunning {genre.lower()} will leave you breathless as {protagonist} fights for {goal}.",
]

PROTAGONISTS = [
    "a lone hero", "a brilliant detective", "an unlikely hero", "a determined woman",
    "a broken man", "a fearless warrior", "a young dreamer", "a wise mentor",
    "a rebellious child", "an ambitious inventor", "a lost soul", "a mysterious stranger",
]

GOALS = [
    "truth", "love", "justice", "freedom", "redemption", "revenge", "knowledge",
    "survival", "immortality", "power", "peace", "hope"
]


# ============================================================================
# ASYNC DATABASE CONNECTION
# ============================================================================

async def get_database() -> AsyncIOMotorDatabase:
    """Connect to MongoDB"""
    client = motor.AsyncIOMotorClient("mongodb://localhost:27017")
    return client["movie_recommendation"]


# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

def generate_movies(count: int = 2000) -> list:
    """
    Generate realistic movie data.
    
    Args:
        count: Number of movies to generate
        
    Returns:
        List of movie documents
    """
    print(f"[SEEDING] Generating {count} movies...")
    
    movies = []
    current_year = datetime.now().year
    
    for i in range(count):
        # Select random genres (1-3 per movie)
        n_genres = random.choices([1, 2, 3], weights=[40, 40, 20])[0]
        movie_genres = random.sample(GENRES, n_genres)
        
        # Random year (1970-2024)
        year = random.randint(1970, current_year)
        
        # Generate title
        title = f"{random.choice(MOVIE_TITLES)} {i+1}" if i > 0 else random.choice(MOVIE_TITLES)
        
        # Generate realistic rating (skewed toward higher ratings)
        rating = round(random.gauss(6.5, 1.5), 1)  # Mean 6.5, Stdev 1.5
        rating = max(0.0, min(10.0, rating))  # Clamp to 0-10
        
        # Generate description
        protagonist = random.choice(PROTAGONISTS)
        goal = random.choice(GOALS)
        genre = movie_genres[0]
        description = random.choice(DESCRIPTIONS_TEMPLATES).format(
            protagonist=protagonist,
            goal=goal,
            genre=genre
        )
        
        movie = {
            "title": title,
            "genre": movie_genres,
            "year": year,
            "rating": rating,
            "description": description,
            "poster_url": f"https://via.placeholder.com/300x450?text={title.replace(' ', '+')[:30]}",
            "trailer_url": None,
            "created_at": datetime.utcnow()
        }
        movies.append(movie)
    
    print(f"[SEEDING] ✓ Generated {count} movies")
    return movies


def generate_users(count: int = 150) -> list:
    """
    Generate user data.
    
    Args:
        count: Number of users to generate
        
    Returns:
        List of user documents
    """
    print(f"[SEEDING] Generating {count} users...")
    
    users = []
    for i in range(count):
        user = {
            "name": f"User{i+1}",
            "email": f"user{i+1}@example.com",
            "password": "hashed_password_placeholder",  # In real code, use argon2
            "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 365))
        }
        users.append(user)
    
    print(f"[SEEDING] ✓ Generated {count} users")
    return users


def generate_ratings(users: list, movies: list, min_ratings: int = 50, max_ratings: int = 150) -> list:
    """
    Generate realistic rating data with heavy-tail distribution.
    
    Distribution: Some users rate many movies (20-30%), most rate fewer (50-80%).
    Each movie gets rated by 2-50 different users.
    Ratings skew toward higher values (realistic user bias).
    
    Args:
        users: List of user documents
        movies: List of movie documents
        min_ratings: Min ratings per user
        max_ratings: Max ratings per user
        
    Returns:
        List of rating documents
    """
    print(f"[SEEDING] Generating ratings (heavy-tail distribution)...")
    
    ratings = []
    user_ids = [str(i) for i in range(len(users))]
    movie_ids = [str(i) for i in range(len(movies))]
    
    # Track ratings per movie to ensure variety
    movie_rating_count = {mid: 0 for mid in movie_ids}
    
    # Create a rating matrix tracker to avoid duplicates
    user_movie_pairs = set()
    
    for user_id in user_ids:
        # Heavy-tail: 30% of users rate many movies, 70% rate fewer
        if random.random() < 0.3:
            # Heavy users: 100-150 ratings
            num_ratings = random.randint(100, min(150, len(movies)))
        else:
            # Light users: 10-40 ratings
            num_ratings = random.randint(10, 40)
        
        # Randomly select movies for this user to rate
        movies_to_rate = random.sample(movie_ids, num_ratings)
        
        for movie_id in movies_to_rate:
            # Skip if already rated
            if (user_id, movie_id) in user_movie_pairs:
                continue
            
            # Generate rating: skewed toward higher values
            rating = round(random.gauss(7.0, 1.8), 1)  # Mean 7.0, slightly higher skew
            rating = max(1, min(10, rating))  # Clamp to 1-10
            
            rating_doc = {
                "user_id": user_id,
                "movie_id": movie_id,
                "rating": rating,
                "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 365))
            }
            
            ratings.append(rating_doc)
            user_movie_pairs.add((user_id, movie_id))
            movie_rating_count[movie_id] += 1
    
    # Ensure each movie is rated by at least 2 users
    unrated_movies = [m for m, count in movie_rating_count.items() if count == 0]
    for movie_id in unrated_movies:
        for _ in range(random.randint(2, 5)):
            user_id = random.choice(user_ids)
            if (user_id, movie_id) not in user_movie_pairs:
                rating_doc = {
                    "user_id": user_id,
                    "movie_id": movie_id,
                    "rating": round(random.gauss(7.0, 1.8), 1),
                    "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 365))
                }
                ratings.append(rating_doc)
                user_movie_pairs.add((user_id, movie_id))
    
    print(f"[SEEDING] ✓ Generated {len(ratings)} ratings")
    print(f"[SEEDING]   • Avg ratings per user: {len(ratings) / len(users):.0f}")
    print(f"[SEEDING]   • Avg ratings per movie: {len(ratings) / len(movies):.0f}")
    
    return ratings


# ============================================================================
# DATABASE OPERATIONS
# ============================================================================

async def seed_database():
    """Main seeding function"""
    
    print("\n" + "="*70)
    print("MOVIE RECOMMENDATION SYSTEM - DATA SEEDING")
    print("="*70 + "\n")
    
    try:
        # Connect to database
        db = await get_database()
        
        # Clear existing data
        print("[SEEDING] Clearing existing collections...")
        await db.users.delete_many({})
        await db.movies.delete_many({})
        await db.ratings.delete_many({})
        await db.favorites.delete_many({})
        print("[SEEDING] ✓ Collections cleared\n")
        
        # Generate data
        movies_data = generate_movies(2000)
        users_data = generate_users(150)
        ratings_data = generate_ratings(users_data, movies_data)
        
        # Insert data
        print("\n[SEEDING] Inserting data into MongoDB...")
        
        # Insert movies
        movies_result = await db.movies.insert_many(movies_data)
        print(f"[SEEDING] ✓ Inserted {len(movies_result.inserted_ids)} movies")
        
        # Insert users
        users_result = await db.users.insert_many(users_data)
        print(f"[SEEDING] ✓ Inserted {len(users_result.inserted_ids)} users")
        
        # Convert inserted IDs for ratings
        movie_ids_map = {str(i): str(oid) for i, oid in enumerate(movies_result.inserted_ids)}
        user_ids_map = {str(i): str(oid) for i, oid in enumerate(users_result.inserted_ids)}
        
        # Update rating documents with actual ObjectIds
        for rating in ratings_data:
            rating['movie_id'] = movie_ids_map[rating['movie_id']]
            rating['user_id'] = user_ids_map[rating['user_id']]
        
        # Insert ratings
        ratings_result = await db.ratings.insert_many(ratings_data)
        print(f"[SEEDING] ✓ Inserted {len(ratings_result.inserted_ids)} ratings")
        
        # Create indexes for performance
        print("\n[SEEDING] Creating database indexes...")
        await db.ratings.create_index("user_id")
        await db.ratings.create_index("movie_id")
        await db.ratings.create_index([("user_id", 1), ("movie_id", 1)], unique=True)
        await db.movies.create_index("genre")
        await db.users.create_index("email", unique=True)
        print("[SEEDING] ✓ Indexes created")
        
        # Print statistics
        print("\n" + "="*70)
        print("SEEDING COMPLETE - DATABASE STATISTICS")
        print("="*70)
        print(f"Movies:       {len(movies_result.inserted_ids):,}")
        print(f"Users:        {len(users_result.inserted_ids):,}")
        print(f"Ratings:      {len(ratings_result.inserted_ids):,}")
        print(f"Avg ratings/user:  {len(ratings_result.inserted_ids) / len(users_result.inserted_ids):.0f}")
        print(f"Avg ratings/movie: {len(ratings_result.inserted_ids) / len(movies_result.inserted_ids):.1f}")
        print("="*70 + "\n")
        
        print("[SEEDING] 🎉 Database ready for ML model training!")
        print("[SEEDING] The collaborative filtering model should now activate automatically.\n")
        
    except Exception as e:
        print(f"\n[ERROR] Seeding failed: {str(e)}")
        raise
    finally:
        # Note: In production, we'd close the connection here
        pass


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    asyncio.run(seed_database())
