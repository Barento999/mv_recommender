"""
Cold Start Handler

Handles recommendations for new users and new items.
Implements multiple strategies for cold start problems.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ColdStartHandler:
    """Handle cold start problems in recommendation systems."""
    
    def __init__(self, strategy: str = 'popularity'):
        """
        Initialize cold start handler.
        
        Args:
            strategy: 'popularity', 'random', 'genre', 'similarity'
        """
        self.strategy = strategy
        self.movies_df: Optional[pd.DataFrame] = None
        self.ratings_df: Optional[pd.DataFrame] = None
        self.user_features: Optional[pd.DataFrame] = None
    
    def setup(self, movies_df: pd.DataFrame, ratings_df: pd.DataFrame) -> None:
        """
        Setup handler with data.
        
        Args:
            movies_df: Movie metadata
            ratings_df: Ratings data
        """
        self.movies_df = movies_df
        self.ratings_df = ratings_df
        logger.info(f"[ColdStart] Handler setup with {len(movies_df)} movies")
    
    def handle_new_user(self, user_profile: Dict = None, limit: int = 10) -> List[Tuple[str, float]]:
        """
        Get recommendations for a new user (no rating history).
        
        Args:
            user_profile: Optional profile dict with 'favorite_genres', 'age', etc.
            limit: Number of recommendations
            
        Returns:
            List of (movie_id, score) tuples
        """
        logger.info(f"[ColdStart] Handling new user with strategy: {self.strategy}")
        
        if self.movies_df is None or len(self.movies_df) == 0:
            logger.warning("[ColdStart] No movie data available")
            return []
        
        if self.strategy == 'popularity':
            return self._recommend_popular(limit)
        elif self.strategy == 'genre' and user_profile and 'favorite_genres' in user_profile:
            return self._recommend_by_genre(user_profile['favorite_genres'], limit)
        elif self.strategy == 'random':
            return self._recommend_random(limit)
        else:
            return self._recommend_popular(limit)  # Default
    
    def handle_new_item(self, movie_id: str, movie_data: Dict, 
                       similar_movies_model = None, limit: int = 10) -> List[Tuple[str, float]]:
        """
        Get initial recommendations for a new movie (no ratings yet).
        
        Args:
            movie_id: ID of new movie
            movie_data: Movie metadata dict
            similar_movies_model: Model to find similar movies
            limit: Number of recommendations
            
        Returns:
            List of users likely to rate this movie
        """
        logger.info(f"[ColdStart] Handling new item: {movie_id}")
        
        if self.strategy == 'similarity' and similar_movies_model:
            return self._recommend_via_similarity(movie_id, similar_movies_model, limit)
        else:
            return self._recommend_popular_users(movie_id, limit)
    
    def _recommend_popular(self, limit: int) -> List[Tuple[str, float]]:
        """Recommend popular (highest rated) movies."""
        try:
            # Get average rating for each movie
            avg_ratings = self.ratings_df.groupby('movie_id')['rating'].mean().to_dict()
            
            # Get movie info
            recommendations = []
            for _, movie in self.movies_df.iterrows():
                movie_id = movie['movie_id']
                rating = avg_ratings.get(movie_id, movie.get('rating', 5.0))
                recommendations.append((movie_id, float(rating)))
            
            # Sort by rating and return top-k
            recommendations.sort(key=lambda x: x[1], reverse=True)
            
            logger.info(f"[ColdStart] Recommending {limit} popular movies")
            return recommendations[:limit]
        
        except Exception as e:
            logger.error(f"[ColdStart] Error in popularity recommendation: {str(e)}")
            return []
    
    def _recommend_by_genre(self, favorite_genres: List[str], limit: int) -> List[Tuple[str, float]]:
        """Recommend movies matching user's favorite genres."""
        try:
            recommendations = []
            
            # Get average rating for each movie
            avg_ratings = self.ratings_df.groupby('movie_id')['rating'].mean().to_dict()
            
            # Find movies in favorite genres
            for _, movie in self.movies_df.iterrows():
                genres = str(movie.get('genre', '')).split('|')
                genres = [g.strip() for g in genres]
                
                # Check if any genre matches
                if any(genre in favorite_genres for genre in genres):
                    movie_id = movie['movie_id']
                    rating = avg_ratings.get(movie_id, movie.get('rating', 5.0))
                    recommendations.append((movie_id, float(rating)))
            
            # Sort by rating
            recommendations.sort(key=lambda x: x[1], reverse=True)
            
            logger.info(f"[ColdStart] Recommending {len(recommendations)} movies by genre")
            return recommendations[:limit]
        
        except Exception as e:
            logger.error(f"[ColdStart] Error in genre-based recommendation: {str(e)}")
            return self._recommend_popular(limit)
    
    def _recommend_random(self, limit: int) -> List[Tuple[str, float]]:
        """Recommend random movies."""
        try:
            sample = self.movies_df.sample(min(limit, len(self.movies_df)))
            recommendations = [
                (row['movie_id'], float(row.get('rating', 5.0)))
                for _, row in sample.iterrows()
            ]
            logger.info(f"[ColdStart] Recommending {len(recommendations)} random movies")
            return recommendations
        
        except Exception as e:
            logger.error(f"[ColdStart] Error in random recommendation: {str(e)}")
            return []
    
    def _recommend_via_similarity(self, movie_id: str, similarity_model, 
                                 limit: int) -> List[Tuple[str, float]]:
        """Get users who rated similar movies."""
        try:
            # Get similar movies
            similar = similarity_model.get_similar_movies(movie_id, limit=limit*2)
            
            # Get users who rated similar movies
            similar_movie_ids = [m_id for m_id, _ in similar]
            
            interested_users = self.ratings_df[
                self.ratings_df['movie_id'].isin(similar_movie_ids)
            ]['user_id'].unique()
            
            # Assign scores based on how many similar movies they rated
            user_scores = {}
            for user_id in interested_users:
                user_ratings = self.ratings_df[self.ratings_df['user_id'] == user_id]
                match_count = len(user_ratings[user_ratings['movie_id'].isin(similar_movie_ids)])
                user_scores[user_id] = match_count / len(similar_movie_ids) if similar_movie_ids else 0
            
            recommendations = sorted(
                user_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:limit]
            
            logger.info(f"[ColdStart] Found {len(recommendations)} interested users")
            return recommendations
        
        except Exception as e:
            logger.error(f"[ColdStart] Error in similarity-based recommendation: {str(e)}")
            return []
    
    def _recommend_popular_users(self, movie_id: str, limit: int) -> List[Tuple[str, float]]:
        """Recommend to popular (active) users."""
        try:
            # Get users sorted by rating activity
            user_activity = self.ratings_df.groupby('user_id').size().to_dict()
            
            recommendations = sorted(
                user_activity.items(),
                key=lambda x: x[1],
                reverse=True
            )[:limit]
            
            logger.info(f"[ColdStart] Recommending to {len(recommendations)} active users")
            return recommendations
        
        except Exception as e:
            logger.error(f"[ColdStart] Error in popular users recommendation: {str(e)}")
            return []
    
    def get_user_profile_from_ratings(self, ratings: List[Tuple[str, float]]) -> Dict:
        """
        Extract user profile from their ratings.
        
        Args:
            ratings: List of (movie_id, rating) tuples
            
        Returns:
            User profile dict
        """
        try:
            if not ratings or self.movies_df is None:
                return {}
            
            rated_movies = self.movies_df[self.movies_df['movie_id'].isin([m for m, _ in ratings])]
            
            # Favorite genres
            all_genres = []
            for _, movie in rated_movies.iterrows():
                genres = str(movie.get('genre', '')).split('|')
                all_genres.extend([g.strip() for g in genres])
            
            favorite_genres = pd.Series(all_genres).value_counts().head(3).index.tolist()
            
            # Average rating preference
            avg_rating = np.mean([r for _, r in ratings])
            
            profile = {
                'favorite_genres': favorite_genres,
                'avg_rating': float(avg_rating),
                'n_ratings': len(ratings),
            }
            
            logger.info(f"[ColdStart] Extracted user profile: {profile}")
            return profile
        
        except Exception as e:
            logger.error(f"[ColdStart] Error extracting user profile: {str(e)}")
            return {}
