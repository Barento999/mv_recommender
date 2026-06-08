"""
Feature Engineering Module

Handles feature extraction, normalization, and transformation.
Prepares data for ML models.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Feature engineering and preprocessing."""
    
    def __init__(self):
        """Initialize feature engineer."""
        self.scalers: Dict = {}
        self.feature_stats: Dict = {}
        self.is_fitted = False
    
    def extract_rating_features(self, ratings_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features from ratings.
        
        Features:
        - rating (original)
        - rating_norm (0-1 normalized)
        - rating_binary (> 5.0 = 1, else 0)
        - time_decay (older ratings weighted less)
        
        Args:
            ratings_df: DataFrame with rating data
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("[FeatureEngineer] Extracting rating features...")
        
        try:
            df = ratings_df.copy()
            
            # Normalize rating to 0-1
            df['rating_norm'] = (df['rating'] - df['rating'].min()) / (df['rating'].max() - df['rating'].min())
            
            # Binary rating (liked/disliked)
            df['rating_binary'] = (df['rating'] > 5.0).astype(int)
            
            # Time-based decay (if timestamp exists)
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                now = pd.Timestamp.now()
                df['days_ago'] = (now - df['timestamp']).dt.days
                df['time_decay'] = np.exp(-df['days_ago'] / 365)  # Decay factor
            else:
                df['time_decay'] = 1.0
            
            # Weighted rating (rating * time_decay)
            df['weighted_rating'] = df['rating'] * df['time_decay']
            
            logger.info("[FeatureEngineer] ✓ Extracted rating features")
            return df
        
        except Exception as e:
            logger.error(f"[FeatureEngineer] Error extracting rating features: {str(e)}")
            return ratings_df
    
    def extract_user_features(self, ratings_df: pd.DataFrame, movies_df: pd.DataFrame = None) -> pd.DataFrame:
        """
        Extract user-level features.
        
        Features:
        - n_ratings: Number of ratings by user
        - avg_rating: Average rating given
        - rating_std: Standard deviation of ratings
        - rating_range: Max - Min rating
        - favorite_genre: Most common genre
        - rating_frequency: Ratings per time period
        
        Args:
            ratings_df: DataFrame with rating data
            movies_df: Optional movie metadata
            
        Returns:
            DataFrame with user features
        """
        logger.info("[FeatureEngineer] Extracting user features...")
        
        try:
            user_features = []
            
            for user_id in ratings_df['user_id'].unique():
                user_ratings = ratings_df[ratings_df['user_id'] == user_id]
                ratings = user_ratings['rating'].values
                
                features = {
                    'user_id': user_id,
                    'n_ratings': len(user_ratings),
                    'avg_rating': float(ratings.mean()),
                    'rating_std': float(ratings.std()) if len(ratings) > 1 else 0.0,
                    'rating_min': float(ratings.min()),
                    'rating_max': float(ratings.max()),
                    'rating_range': float(ratings.max() - ratings.min()),
                    'rating_median': float(np.median(ratings)),
                }
                
                user_features.append(features)
            
            df = pd.DataFrame(user_features)
            logger.info(f"[FeatureEngineer] ✓ Extracted features for {len(df)} users")
            
            return df
        
        except Exception as e:
            logger.error(f"[FeatureEngineer] Error extracting user features: {str(e)}")
            return pd.DataFrame()
    
    def extract_movie_features(self, ratings_df: pd.DataFrame, movies_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract movie-level features.
        
        Features:
        - n_ratings: Number of ratings received
        - avg_rating: Average rating
        - rating_std: Std deviation
        - rating_count_trend: Recent vs overall ratings
        - popularity_score: n_ratings * avg_rating
        
        Args:
            ratings_df: DataFrame with rating data
            movies_df: DataFrame with movie metadata
            
        Returns:
            DataFrame with movie features
        """
        logger.info("[FeatureEngineer] Extracting movie features...")
        
        try:
            movie_features = []
            
            for _, movie in movies_df.iterrows():
                movie_id = movie['movie_id']
                movie_ratings = ratings_df[ratings_df['movie_id'] == movie_id]
                
                if len(movie_ratings) == 0:
                    ratings = np.array([movie.get('rating', 5.0)])
                else:
                    ratings = movie_ratings['rating'].values
                
                features = {
                    'movie_id': movie_id,
                    'title': movie.get('title', ''),
                    'year': movie.get('year', 2000),
                    'base_rating': float(movie.get('rating', 5.0)),
                    'n_ratings': len(movie_ratings),
                    'avg_user_rating': float(ratings.mean()),
                    'rating_std': float(ratings.std()) if len(ratings) > 1 else 0.0,
                    'popularity_score': len(movie_ratings) * float(ratings.mean()),
                    'rating_consistency': 1.0 - (float(ratings.std()) / 10.0) if len(ratings) > 1 else 1.0,
                }
                
                movie_features.append(features)
            
            df = pd.DataFrame(movie_features)
            logger.info(f"[FeatureEngineer] ✓ Extracted features for {len(df)} movies")
            
            return df
        
        except Exception as e:
            logger.error(f"[FeatureEngineer] Error extracting movie features: {str(e)}")
            return pd.DataFrame()
    
    def normalize_features(self, df: pd.DataFrame, method: str = 'minmax', 
                          columns: List[str] = None) -> Tuple[pd.DataFrame, Dict]:
        """
        Normalize features using MinMax or Standard scaling.
        
        Args:
            df: DataFrame with features
            method: 'minmax' or 'standard'
            columns: Columns to normalize (all numeric if None)
            
        Returns:
            Tuple of (normalized_df, scaler_params)
        """
        logger.info(f"[FeatureEngineer] Normalizing features ({method})...")
        
        try:
            df_norm = df.copy()
            
            if columns is None:
                columns = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if method == 'minmax':
                scaler = MinMaxScaler()
            else:
                scaler = StandardScaler()
            
            df_norm[columns] = scaler.fit_transform(df[columns])
            
            # Store scaler for later
            scaler_params = {
                'method': method,
                'columns': columns,
                'scale': getattr(scaler, 'scale_', None),
                'min': getattr(scaler, 'data_min_', None),
            }
            
            logger.info(f"[FeatureEngineer] ✓ Normalized {len(columns)} columns")
            
            return df_norm, scaler_params
        
        except Exception as e:
            logger.error(f"[FeatureEngineer] Error normalizing features: {str(e)}")
            return df, {}
    
    def create_interaction_features(self, user_features: pd.DataFrame, 
                                   movie_features: pd.DataFrame) -> pd.DataFrame:
        """
        Create interaction features between users and movies.
        
        Args:
            user_features: User feature DataFrame
            movie_features: Movie feature DataFrame
            
        Returns:
            DataFrame with interaction features
        """
        logger.info("[FeatureEngineer] Creating interaction features...")
        
        try:
            interactions = []
            
            for _, user in user_features.iterrows():
                for _, movie in movie_features.iterrows():
                    interaction = {
                        'user_id': user['user_id'],
                        'movie_id': movie['movie_id'],
                        'user_avg_rating': user['avg_rating'],
                        'movie_avg_rating': movie['avg_user_rating'],
                        'rating_diff': abs(user['avg_rating'] - movie['avg_user_rating']),
                        'user_popularity': user['n_ratings'],
                        'movie_popularity': movie['n_ratings'],
                        'combined_popularity': user['n_ratings'] * movie['n_ratings'],
                    }
                    interactions.append(interaction)
            
            df = pd.DataFrame(interactions)
            logger.info(f"[FeatureEngineer] ✓ Created {len(df)} interaction features")
            
            return df
        
        except Exception as e:
            logger.error(f"[FeatureEngineer] Error creating interaction features: {str(e)}")
            return pd.DataFrame()
