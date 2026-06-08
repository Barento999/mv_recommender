"""
Synchronous Data Seeding Script: 2000 Movies + Realistic Ratings

This is a simpler version that works with synchronous PyMongo.
Use this if you're running MongoDB locally without Docker.

Requirements:
- MongoDB running on localhost:27017 (or specify MONGODB_URL in .env)
- Python venv activated
- Dependencies: pip install -r requirements.txt

Usage:
    python seed_2000_movies_sync.py
"""

import random
import sys
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


# ============================================================================
# DATA CONSTANTS
# ============================================================================

GENRES = [
    "Action", "Comedy", "Drama", "Horror", "Thriller", "Sci-Fi", "Fantasy",
    "Romance", "Animation", "Adventure", "Crime", "Documentary", "Family",
    "History", "Mystery", "Western", "War", "Sport", "Musical", "Biography"
]

MOVIE_TITLES = [
    # Action (15)
    "Velocity Vortex", "Shadow Protocol", "Midnight Strike", "Quantum Breach",
    "Phoenix Rising", "Silent Reckoning", "Chaos Theory", "Iron Guardian",
    "Lethal Alliance", "Fortress Unbreakable", "Thunder Down", "Apex Predator",
    "Neon Nights", "Digital Storm", "Final Verdict",
    
    # Drama (15)
    "Echoes of Tomorrow", "Fractured Dreams", "Crossroads Destiny", "Silent Witness",
    "Breaking Point", "The Last Goodbye", "Redemption Road", "Unraveled Hearts",
    "The Weight of Years", "Forgotten Souls", "Shattered Reflections", "Beneath the Surface",
    "Hidden Truths", "Fading Light", "Open Hearts",
    
    # Comedy (15)
    "Laughing Matter", "Chaos Control", "Blissful Chaos", "Perfect Timing",
    "The Awkward Truth", "Love's Misfortune", "Dating Disasters", "Friends Forever",
    "Weekend Getaway", "Office Legends", "Road Trip Chronicles", "Wedding Bells",
    "Mistaken Identity", "Comedy Gold", "Hilarious Mishaps",
    
    # Sci-Fi (15)
    "Neural Nexus", "Temporal Shift", "The Last Horizon", "Digital Dreams",
    "Void Explorer", "Infinite Loop", "Cosmic Collision", "Future Wars",
    "Time Paradox", "Cyber Awakening", "The Singularity Event", "Dimensional Breach",
    "Stargate Protocol", "Quantum Leap", "Space Odyssey",
    
    # Horror (12)
    "Midnight Terror", "The Haunting", "Crimson Shadows", "Fear Manifest",
    "The Descent", "Nightmare Realm", "Curse of the Forgotten", "The Awakening",
    "Darkness Calls", "The Reckoning", "Possessed", "Final Scream",
]

DESCRIPTIONS_TEMPLATES = [
    "An epic tale of {genre.lower()} following {protagonist} as they face their greatest challenge yet.",
    "When {protagonist} discovers a life-changing secret, everything falls apart in this gripping {genre.lower()}.",
    "A thrilling {genre.lower()} about {protagonist}'s quest for {goal}.",
    "In this powerful {genre.lower()}, {protagonist} must overcome impossible odds to {goal}.",
    "A compelling story about {protagonist} learning to {goal} in this {genre.lower()} masterpiece.",
    "When darkness falls, only {protagonist} can save the day in this intense {genre.lower()}.",
]

PROTAGONISTS = [
    "a lone hero", "a brilliant detective", "an unlikely hero", "a determined woman",
    "a broken man", "a fearless warrior", "a young dreamer", "a wise mentor",
]

GOALS = [
    "truth", "love", "justice", "freedom", "redemption", "revenge", "knowledge",
    "survival", "immortality", "power", "peace", "hope"
]


# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

def generate_movies(count: int = 2000) -> list:
    """Generate realistic movie data."""
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
        base_title = random.choice(MOVIE_TITLES)
        title = f"{base_title} {i+1}" if i > len(MOVIE_TITLES) else base_title
        
        # Generate realistic rating (skewed toward higher ratings)
        rating = round(random.gauss(6.5, 1.5), 1)
        rating = max(0.0, min(10.0, rating))
        
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
    """Generate user data."""
    print(f"[SEEDING] Generating {count} users...")
    
    users = []
    for i in range(count):
        user = {
            "name": f"User{i+1}",
            "email": f"user{i+1}@example.com",
            "password": "hashed_password_placeholder",
            "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 365))
        }
        users.append(user)
    
    print(f"[SEEDING] ✓ Generated {count} users")
    return users


def generate_ratings(users: list, movies: list, min_per_user: int = 50, max_per_user: int = 150) -> list:
    """Generate realistic rating data with heavy-tail distribution."""
    print(f"[SEEDING] Generating ratings (heavy-tail distribution)...")
    
    ratings = []
    user_ids = [str(i) for i in range(len(users))]
    movie_ids = [str(i) for i in range(len(movies))]
    
    movie_rating_count = {mid: 0 for mid in movie_ids}
    user_movie_pairs = set()
    
    for user_id in user_ids:
        # Heavy-tail: 30% of users rate many movies
        if random.random() < 0.3:
            num_ratings = random.randint(100, min(150, len(movies)))
        else:
            num_ratings = random.randint(10, 40)
        
        # Randomly select movies for this user to rate
        movies_to_rate = random.sample(movie_ids, min(num_ratings, len(movie_ids)))
        
        for movie_id in movies_to_rate:
            if (user_id, movie_id) in user_movie_pairs:
                continue
            
            # Generate rating: skewed toward higher values
            rating = round(random.gauss(7.0, 1.8), 1)
            rating = max(1, min(10, rating))
            
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
# MAIN SEEDING FUNCTION
# ============================================================================

def seed_database():
    """Main seeding function."""
    
    print("\n" + "="*70)
    print("MOVIE RECOMMENDATION SYSTEM - DATA SEEDING (SYNC)")
    print("="*70 + "\n")
    
    try:
        # Connect to MongoDB
        print("[SEEDING] Connecting to MongoDB at localhost:27017...")
        try:
            client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            print("[SEEDING] ✓ Connected to MongoDB\n")
        except ServerSelectionTimeoutError:
            print("[ERROR] Cannot connect to MongoDB at localhost:27017")
            print("[ERROR] Please start MongoDB first:")
            print("        • Docker: docker compose up -d")
            print("        • Local: mongod --dbpath /path/to/data")
            sys.exit(1)
        
        db = client["movie_recommendation"]
        
        # Clear existing data
        print("[SEEDING] Clearing existing collections...")
        db.users.delete_many({})
        db.movies.delete_many({})
        db.ratings.delete_many({})
        db.favorites.delete_many({})
        print("[SEEDING] ✓ Collections cleared\n")
        
        # Generate data
        movies_data = generate_movies(2000)
        users_data = generate_users(150)
        ratings_data = generate_ratings(users_data, movies_data)
        
        # Insert data
        print("\n[SEEDING] Inserting data into MongoDB...")
        
        # Insert movies
        movies_result = db.movies.insert_many(movies_data)
        print(f"[SEEDING] ✓ Inserted {len(movies_result.inserted_ids)} movies")
        
        # Insert users
        users_result = db.users.insert_many(users_data)
        print(f"[SEEDING] ✓ Inserted {len(users_result.inserted_ids)} users")
        
        # Create mapping from string index to ObjectId
        movie_ids_map = {str(i): str(oid) for i, oid in enumerate(movies_result.inserted_ids)}
        user_ids_map = {str(i): str(oid) for i, oid in enumerate(users_result.inserted_ids)}
        
        # Update rating documents with actual ObjectIds
        for rating in ratings_data:
            rating['movie_id'] = movie_ids_map[rating['movie_id']]
            rating['user_id'] = user_ids_map[rating['user_id']]
        
        # Insert ratings
        ratings_result = db.ratings.insert_many(ratings_data)
        print(f"[SEEDING] ✓ Inserted {len(ratings_result.inserted_ids)} ratings")
        
        # Create indexes
        print("\n[SEEDING] Creating database indexes...")
        db.ratings.create_index("user_id")
        db.ratings.create_index("movie_id")
        db.ratings.create_index([("user_id", 1), ("movie_id", 1)], unique=True)
        db.movies.create_index("genre")
        db.users.create_index("email", unique=True)
        print("[SEEDING] ✓ Indexes created")
        
        # Print statistics
        print("\n" + "="*70)
        print("SEEDING COMPLETE - DATABASE STATISTICS")
        print("="*70)
        print(f"Movies:           {len(movies_result.inserted_ids):,}")
        print(f"Users:            {len(users_result.inserted_ids):,}")
        print(f"Ratings:          {len(ratings_result.inserted_ids):,}")
        print(f"Avg ratings/user: {len(ratings_result.inserted_ids) / len(users_result.inserted_ids):.0f}")
        print(f"Avg ratings/movie:{len(ratings_result.inserted_ids) / len(movies_result.inserted_ids):.1f}")
        print("="*70 + "\n")
        
        print("[SEEDING] 🎉 Database ready for ML model training!")
        print("[SEEDING] The collaborative filtering model will activate automatically.\n")
        
        client.close()
        
    except Exception as e:
        print(f"\n[ERROR] Seeding failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    seed_database()
