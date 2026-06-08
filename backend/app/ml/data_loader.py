"""
ML Data Loader Module

Handles loading and validation of CSV data for the recommendation system.
Provides a clean interface for:
- Loading movies from CSV
- Loading users from CSV
- Loading ratings from CSV
- Validating data integrity
- Converting to model-ready formats
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Load and validate CSV data for ML pipeline."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize data loader.
        
        Args:
            data_dir: Directory containing CSV files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.movies_df: Optional[pd.DataFrame] = None
        self.users_df: Optional[pd.DataFrame] = None
        self.ratings_df: Optional[pd.DataFrame] = None
        
    def load_movies(self, filepath: str = None) -> pd.DataFrame:
        """
        Load movies from CSV.
        
        Expected columns:
        - movie_id (str, unique)
        - title (str)
        - genre (str, comma-separated or pipe-separated)
        - year (int)
        - rating (float, 0-10)
        - description (str, optional)
        - poster_url (str, optional)
        
        Args:
            filepath: Path to CSV file (defaults to data/movies.csv)
            
        Returns:
            Validated movies DataFrame
        """
        if filepath is None:
            filepath = str(self.data_dir / "movies.csv")
        
        logger.info(f"[DataLoader] Loading movies from: {filepath}")
        
        try:
            df = pd.read_csv(filepath)
            
            # Validate required columns
            required_cols = ['movie_id', 'title', 'genre', 'year', 'rating']
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                raise ValueError(f"Missing required columns: {missing}")
            
            # Ensure data types
            df['movie_id'] = df['movie_id'].astype(str)
            df['title'] = df['title'].astype(str)
            df['year'] = df['year'].astype(int)
            df['rating'] = df['rating'].astype(float)
            
            # Validate movie_id uniqueness
            if df['movie_id'].duplicated().any():
                logger.warning("[DataLoader] Duplicate movie_ids found, keeping first occurrence")
                df = df.drop_duplicates(subset=['movie_id'], keep='first')
            
            # Validate rating range
            df['rating'] = df['rating'].clip(0.0, 10.0)
            
            # Validate year range
            current_year = datetime.now().year
            df['year'] = df['year'].clip(1900, current_year)
            
            # Optional columns
            if 'description' not in df.columns:
                df['description'] = ""
            if 'poster_url' not in df.columns:
                df['poster_url'] = ""
            
            self.movies_df = df
            logger.info(f"[DataLoader] ✓ Loaded {len(df)} movies")
            
            return df
            
        except FileNotFoundError:
            logger.error(f"[DataLoader] ✗ File not found: {filepath}")
            raise
        except Exception as e:
            logger.error(f"[DataLoader] ✗ Error loading movies: {str(e)}")
            raise
    
    def load_users(self, filepath: str = None) -> pd.DataFrame:
        """
        Load users from CSV.
        
        Expected columns:
        - user_id (str, unique)
        - name (str)
        - email (str, unique)
        
        Args:
            filepath: Path to CSV file (defaults to data/users.csv)
            
        Returns:
            Validated users DataFrame
        """
        if filepath is None:
            filepath = str(self.data_dir / "users.csv")
        
        logger.info(f"[DataLoader] Loading users from: {filepath}")
        
        try:
            df = pd.read_csv(filepath)
            
            # Validate required columns
            required_cols = ['user_id', 'name', 'email']
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                raise ValueError(f"Missing required columns: {missing}")
            
            # Ensure data types
            df['user_id'] = df['user_id'].astype(str)
            df['name'] = df['name'].astype(str)
            df['email'] = df['email'].astype(str)
            
            # Validate user_id uniqueness
            if df['user_id'].duplicated().any():
                logger.warning("[DataLoader] Duplicate user_ids found, keeping first")
                df = df.drop_duplicates(subset=['user_id'], keep='first')
            
            # Validate email uniqueness
            if df['email'].duplicated().any():
                logger.warning("[DataLoader] Duplicate emails found, keeping first")
                df = df.drop_duplicates(subset=['email'], keep='first')
            
            self.users_df = df
            logger.info(f"[DataLoader] ✓ Loaded {len(df)} users")
            
            return df
            
        except FileNotFoundError:
            logger.error(f"[DataLoader] ✗ File not found: {filepath}")
            raise
        except Exception as e:
            logger.error(f"[DataLoader] ✗ Error loading users: {str(e)}")
            raise
    
    def load_ratings(self, filepath: str = None) -> pd.DataFrame:
        """
        Load ratings from CSV.
        
        Expected columns:
        - user_id (str, foreign key to users)
        - movie_id (str, foreign key to movies)
        - rating (float, 1-10)
        
        Args:
            filepath: Path to CSV file (defaults to data/ratings.csv)
            
        Returns:
            Validated ratings DataFrame
        """
        if filepath is None:
            filepath = str(self.data_dir / "ratings.csv")
        
        logger.info(f"[DataLoader] Loading ratings from: {filepath}")
        
        try:
            df = pd.read_csv(filepath)
            
            # Validate required columns
            required_cols = ['user_id', 'movie_id', 'rating']
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                raise ValueError(f"Missing required columns: {missing}")
            
            # Ensure data types
            df['user_id'] = df['user_id'].astype(str)
            df['movie_id'] = df['movie_id'].astype(str)
            df['rating'] = df['rating'].astype(float)
            
            # Validate rating range
            df['rating'] = df['rating'].clip(1, 10)
            
            # Remove duplicate ratings (keep latest by keeping last)
            initial_count = len(df)
            df = df.drop_duplicates(subset=['user_id', 'movie_id'], keep='last')
            if len(df) < initial_count:
                logger.warning(f"[DataLoader] Removed {initial_count - len(df)} duplicate ratings")
            
            # Validate foreign keys if reference data is loaded
            if self.users_df is not None:
                invalid_users = ~df['user_id'].isin(self.users_df['user_id'])
                if invalid_users.any():
                    logger.warning(f"[DataLoader] Removing {invalid_users.sum()} ratings with invalid user_ids")
                    df = df[~invalid_users]
            
            if self.movies_df is not None:
                invalid_movies = ~df['movie_id'].isin(self.movies_df['movie_id'])
                if invalid_movies.any():
                    logger.warning(f"[DataLoader] Removing {invalid_movies.sum()} ratings with invalid movie_ids")
                    df = df[~invalid_movies]
            
            self.ratings_df = df
            logger.info(f"[DataLoader] ✓ Loaded {len(df)} ratings")
            
            return df
            
        except FileNotFoundError:
            logger.error(f"[DataLoader] ✗ File not found: {filepath}")
            raise
        except Exception as e:
            logger.error(f"[DataLoader] ✗ Error loading ratings: {str(e)}")
            raise
    
    def load_all(self, data_dir: str = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Load all data (movies, users, ratings).
        
        Args:
            data_dir: Directory containing CSV files
            
        Returns:
            Tuple of (movies_df, users_df, ratings_df)
        """
        if data_dir:
            self.data_dir = Path(data_dir)
        
        logger.info(f"[DataLoader] Loading all data from: {self.data_dir}")
        
        # Load in order (users and movies first for validation)
        movies = self.load_movies()
        users = self.load_users()
        ratings = self.load_ratings()
        
        logger.info(f"[DataLoader] ✓ All data loaded successfully")
        logger.info(f"[DataLoader]   • Movies: {len(movies)}")
        logger.info(f"[DataLoader]   • Users: {len(users)}")
        logger.info(f"[DataLoader]   • Ratings: {len(ratings)}")
        
        return movies, users, ratings
    
    def get_data_summary(self) -> Dict:
        """
        Get summary statistics of loaded data.
        
        Returns:
            Dict with statistics
        """
        summary = {}
        
        if self.movies_df is not None:
            summary['movies'] = {
                'count': len(self.movies_df),
                'genres': self.movies_df['genre'].nunique() if 'genre' in self.movies_df else 0,
                'avg_rating': float(self.movies_df['rating'].mean()),
                'year_range': (int(self.movies_df['year'].min()), int(self.movies_df['year'].max()))
            }
        
        if self.users_df is not None:
            summary['users'] = {
                'count': len(self.users_df)
            }
        
        if self.ratings_df is not None:
            summary['ratings'] = {
                'count': len(self.ratings_df),
                'avg_rating': float(self.ratings_df['rating'].mean()),
                'sparsity': 1 - (len(self.ratings_df) / (len(self.users_df) * len(self.movies_df)))
                if self.users_df is not None and self.movies_df is not None else None
            }
        
        return summary
