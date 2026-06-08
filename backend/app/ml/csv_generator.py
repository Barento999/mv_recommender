"""
CSV Data Generator for ML Recommendation System

Generates realistic movie, user, and rating data as CSV files.
Designed for ML training pipelines.
"""

import csv
import random
from pathlib import Path
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class CSVDataGenerator:
    """Generate and export CSV data for ML training."""
    
    GENRES = [
        "Action", "Comedy", "Drama", "Horror", "Thriller", "Sci-Fi", "Fantasy",
        "Romance", "Animation", "Adventure", "Crime", "Documentary", "Family",
        "History", "Mystery", "Western", "War", "Sport", "Musical", "Biography"
    ]
    
    MOVIE_TITLES = [
        "Velocity Vortex", "Shadow Protocol", "Midnight Strike", "Quantum Breach",
        "Phoenix Rising", "Silent Reckoning", "Chaos Theory", "Iron Guardian",
        "Lethal Alliance", "Fortress Unbreakable", "Thunder Down", "Apex Predator",
        "Neon Nights", "Digital Storm", "Final Verdict", "Echoes of Tomorrow",
        "Fractured Dreams", "Crossroads Destiny", "Silent Witness", "Breaking Point",
        "The Last Goodbye", "Redemption Road", "Unraveled Hearts", "The Weight of Years",
        "Forgotten Souls", "Shattered Reflections", "Beneath the Surface", "Hidden Truths",
        "Fading Light", "Open Hearts", "Laughing Matter", "Chaos Control",
        "Blissful Chaos", "Perfect Timing", "The Awkward Truth", "Love's Misfortune",
        "Dating Disasters", "Friends Forever", "Weekend Getaway", "Office Legends",
        "Road Trip Chronicles", "Wedding Bells", "Mistaken Identity", "Comedy Gold",
        "Hilarious Mishaps", "Neural Nexus", "Temporal Shift", "The Last Horizon",
        "Digital Dreams", "Void Explorer", "Infinite Loop", "Cosmic Collision",
        "Future Wars", "Time Paradox", "Cyber Awakening", "The Singularity Event",
        "Dimensional Breach", "Stargate Protocol", "Quantum Leap", "Space Odyssey",
    ]
    
    PROTAGONISTS = [
        "a lone hero", "a brilliant detective", "an unlikely hero", "a determined woman",
        "a broken man", "a fearless warrior", "a young dreamer", "a wise mentor",
    ]
    
    GOALS = [
        "truth", "love", "justice", "freedom", "redemption", "revenge", "knowledge",
        "survival", "immortality", "power", "peace", "hope"
    ]
    
    def __init__(self, output_dir: str = "data"):
        """Initialize generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        logger.info(f"[CSVGenerator] Output directory: {self.output_dir}")
    
    def generate_movies_csv(self, count: int = 2000, filename: str = "movies.csv") -> Path:
        """
        Generate movies CSV file.
        
        Args:
            count: Number of movies to generate
            filename: Output filename
            
        Returns:
            Path to generated file
        """
        filepath = self.output_dir / filename
        logger.info(f"[CSVGenerator] Generating {count} movies...")
        
        current_year = datetime.now().year
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['movie_id', 'title', 'genre', 'year', 'rating', 'description', 'poster_url'])
            
            for i in range(count):
                movie_id = f"m{i:05d}"
                
                # Random genres (1-3)
                n_genres = random.choices([1, 2, 3], weights=[40, 40, 20])[0]
                genres = '|'.join(random.sample(self.GENRES, n_genres))
                
                # Title
                base_title = random.choice(self.MOVIE_TITLES)
                title = f"{base_title} {i}" if i > 0 else base_title
                
                # Year
                year = random.randint(1970, current_year)
                
                # Rating (skewed toward higher)
                rating = round(random.gauss(6.5, 1.5), 1)
                rating = max(0.0, min(10.0, rating))
                
                # Description
                protagonist = random.choice(self.PROTAGONISTS)
                goal = random.choice(self.GOALS)
                desc = f"A thrilling story following {protagonist} in quest for {goal}."
                
                # Poster URL
                poster_url = f"https://via.placeholder.com/300x450?text={title[:20].replace(' ', '+')}"
                
                writer.writerow([movie_id, title, genres, year, rating, desc, poster_url])
        
        logger.info(f"[CSVGenerator] ✓ Generated {filepath}")
        return filepath
    
    def generate_users_csv(self, count: int = 150, filename: str = "users.csv") -> Path:
        """
        Generate users CSV file.
        
        Args:
            count: Number of users to generate
            filename: Output filename
            
        Returns:
            Path to generated file
        """
        filepath = self.output_dir / filename
        logger.info(f"[CSVGenerator] Generating {count} users...")
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'name', 'email'])
            
            for i in range(count):
                user_id = f"u{i:05d}"
                name = f"User{i+1}"
                email = f"user{i+1}@example.com"
                writer.writerow([user_id, name, email])
        
        logger.info(f"[CSVGenerator] ✓ Generated {filepath}")
        return filepath
    
    def generate_ratings_csv(
        self,
        n_users: int = 150,
        n_movies: int = 2000,
        min_per_user: int = 10,
        max_per_user: int = 150,
        filename: str = "ratings.csv"
    ) -> Path:
        """
        Generate ratings CSV with heavy-tail distribution.
        
        Args:
            n_users: Number of users
            n_movies: Number of movies
            min_per_user: Min ratings per user (casual users)
            max_per_user: Max ratings per user (power users)
            filename: Output filename
            
        Returns:
            Path to generated file
        """
        filepath = self.output_dir / filename
        logger.info(f"[CSVGenerator] Generating ratings (heavy-tail)...")
        
        user_ids = [f"u{i:05d}" for i in range(n_users)]
        movie_ids = [f"m{i:05d}" for i in range(n_movies)]
        
        ratings = []
        user_movie_pairs = set()
        
        for user_id in user_ids:
            # Heavy-tail: 30% power users, 70% casual
            if random.random() < 0.3:
                num_ratings = random.randint(100, min(150, n_movies))
            else:
                num_ratings = random.randint(min_per_user, max_per_user)
            
            movies_to_rate = random.sample(movie_ids, min(num_ratings, n_movies))
            
            for movie_id in movies_to_rate:
                if (user_id, movie_id) in user_movie_pairs:
                    continue
                
                # Rating: skewed toward higher values
                rating = round(random.gauss(7.0, 1.8), 1)
                rating = max(1, min(10, rating))
                
                ratings.append((user_id, movie_id, rating))
                user_movie_pairs.add((user_id, movie_id))
        
        # Ensure each movie is rated by at least 2 users
        movie_rating_count = {mid: 0 for mid in movie_ids}
        for _, movie_id, _ in ratings:
            movie_rating_count[movie_id] += 1
        
        unrated_movies = [m for m, count in movie_rating_count.items() if count == 0]
        for movie_id in unrated_movies:
            for _ in range(random.randint(2, 5)):
                user_id = random.choice(user_ids)
                if (user_id, movie_id) not in user_movie_pairs:
                    rating = round(random.gauss(7.0, 1.8), 1)
                    ratings.append((user_id, movie_id, rating))
                    user_movie_pairs.add((user_id, movie_id))
        
        # Write to CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'movie_id', 'rating'])
            writer.writerows(ratings)
        
        logger.info(f"[CSVGenerator] ✓ Generated {len(ratings)} ratings in {filepath}")
        
        return filepath
    
    def generate_all_csvs(
        self,
        n_movies: int = 2000,
        n_users: int = 150,
        output_dir: str = None
    ) -> dict:
        """
        Generate all CSV files (movies, users, ratings).
        
        Args:
            n_movies: Number of movies
            n_users: Number of users
            output_dir: Output directory
            
        Returns:
            Dict with paths to generated files
        """
        if output_dir:
            self.output_dir = Path(output_dir)
            self.output_dir.mkdir(exist_ok=True)
        
        logger.info("[CSVGenerator] ===================================")
        logger.info("[CSVGenerator] Generating all CSV data")
        logger.info("[CSVGenerator] ===================================")
        
        movies_path = self.generate_movies_csv(n_movies)
        users_path = self.generate_users_csv(n_users)
        ratings_path = self.generate_ratings_csv(n_users, n_movies)
        
        logger.info("[CSVGenerator] ✓ All CSV files generated successfully")
        
        return {
            'movies': str(movies_path),
            'users': str(users_path),
            'ratings': str(ratings_path),
            'directory': str(self.output_dir)
        }


def generate_csvs(
    n_movies: int = 2000,
    n_users: int = 150,
    output_dir: str = "data"
) -> dict:
    """
    Convenience function to generate all CSVs.
    
    Args:
        n_movies: Number of movies
        n_users: Number of users
        output_dir: Output directory
        
    Returns:
        Dict with paths to generated files
    """
    generator = CSVDataGenerator(output_dir)
    return generator.generate_all_csvs(n_movies, n_users, output_dir)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generator = CSVDataGenerator("data")
    generator.generate_all_csvs(2000, 150)
