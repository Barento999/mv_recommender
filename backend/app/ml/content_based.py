"""
Content-Based Recommendation System

Recommends movies based on movie features (genre, year, rating, etc.)
instead of user-user similarity.

Algorithm: TF-IDF on genres + metadata similarity
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ContentBasedRecommender:
    """Content-based movie recommendation system."""
    
    def __init__(self, model_name: str = "content_based_v1"):
        """
        Initialize content-based recommender.
        
        Args:
            model_name: Name for model versioning
        """
        self.model_name = model_name
        self.model_version = "1.0.0"
        self.is_trained = False
        
        # Movie data
        self.movies_df: Optional[pd.DataFrame] = None
        self.movie_ids: Optional[List[str]] = None
        
        # Feature vectors
        self.feature_matrix: Optional[np.ndarray] = None
        self.tfidf_vectorizer: Optional[TfidfVectorizer] = None
        
        # Metrics
        self.metrics: Dict = {}
    
    def train(self, movies_df: pd.DataFrame, ratings_df: pd.DataFrame = None) -> bool:
        """
        Train content-based model on movie metadata.
        
        Args:
            movies_df: DataFrame with columns [movie_id, title, genre, year, rating]
            ratings_df: Optional DataFrame for additional context
            
        Returns:
            True if training successful
        """
        import time
        start_time = time.time()
        
        try:
            logger.info("[ContentBased] Training content-based model...")
            
            if movies_df is None or len(movies_df) == 0:
                logger.error("[ContentBased] No movies data provided")
                return False
            
            self.movies_df = movies_df.copy()
            self.movie_ids = self.movies_df['movie_id'].tolist()
            
            # Create feature string combining genres, year, and normalized rating
            features = []
            for _, row in self.movies_df.iterrows():
                # Extract genres
                genres = str(row.get('genre', '')).split('|')
                genres = [g.strip() for g in genres if g.strip()]
                
                # Year decade
                year = int(row.get('year', 2000))
                decade = f"decade_{year // 10 * 10}s"
                
                # Rating category
                rating = float(row.get('rating', 5.0))
                if rating >= 8.0:
                    rating_cat = "highly_rated"
                elif rating >= 6.0:
                    rating_cat = "well_rated"
                else:
                    rating_cat = "lower_rated"
                
                feature_str = ' '.join(genres + [decade, rating_cat])
                features.append(feature_str)
            
            # TF-IDF vectorization
            self.tfidf_vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            self.feature_matrix = self.tfidf_vectorizer.fit_transform(features).toarray()
            
            # Calculate movie-movie similarity
            movie_similarity = cosine_similarity(self.feature_matrix)
            self.movie_similarity_matrix = movie_similarity
            
            self.is_trained = True
            training_time = time.time() - start_time
            
            self.metrics = {
                'model_name': self.model_name,
                'algorithm': 'Content-Based (TF-IDF)',
                'n_movies': len(self.movies_df),
                'n_features': self.feature_matrix.shape[1],
                'training_time_seconds': training_time,
                'trained_at': time.time()
            }
            
            logger.info(f"[ContentBased] ✓ Training complete ({training_time:.3f}s)")
            logger.info(f"[ContentBased] Movies: {len(self.movie_ids)}, Features: {self.feature_matrix.shape[1]}")
            
            return True
        
        except Exception as e:
            logger.error(f"[ContentBased] ✗ Training failed: {str(e)}")
            return False
    
    async def recommend(self, user_id: str, user_rated_movies: List[str] = None, 
                       limit: int = 10) -> List[Tuple[str, float]]:
        """
        Get content-based recommendations for a user.
        
        Recommends movies similar to movies the user has already rated.
        
        Args:
            user_id: User ID (for logging)
            user_rated_movies: List of movie IDs user has rated
            limit: Number of recommendations
            
        Returns:
            List of (movie_id, score) tuples
        """
        try:
            if not self.is_trained:
                logger.warning("[ContentBased] Model not trained")
                return []
            
            if not user_rated_movies:
                # Cold start: return top-rated movies
                logger.debug(f"[ContentBased] Cold start for {user_id}, returning top movies")
                top_indices = np.argsort(
                    self.movies_df['rating'].values
                )[-limit:][::-1]
                return [
                    (self.movie_ids[i], float(self.movies_df.iloc[i]['rating']))
                    for i in top_indices
                ]
            
            # Find indices of rated movies
            rated_indices = []
            for movie_id in user_rated_movies:
                if movie_id in self.movie_ids:
                    rated_indices.append(self.movie_ids.index(movie_id))
            
            if not rated_indices:
                # Fallback to cold start
                return await self.recommend(user_id, limit=limit)
            
            # Calculate average similarity to rated movies
            avg_similarity = np.zeros(len(self.movie_ids))
            for idx in rated_indices:
                avg_similarity += self.movie_similarity_matrix[idx]
            avg_similarity /= len(rated_indices)
            
            # Filter out already-rated movies
            for idx in rated_indices:
                avg_similarity[idx] = -1
            
            # Get top recommendations
            top_indices = np.argsort(avg_similarity)[-limit:][::-1]
            recommendations = [
                (self.movie_ids[i], float(avg_similarity[i]))
                for i in top_indices
                if avg_similarity[i] >= 0
            ]
            
            return recommendations
        
        except Exception as e:
            logger.error(f"[ContentBased] Error getting recommendations: {str(e)}")
            return []
    
    def get_metrics(self) -> Dict:
        """Return model metrics."""
        return self.metrics.copy()
    
    def get_similar_movies(self, movie_id: str, limit: int = 10) -> List[Tuple[str, float]]:
        """
        Get movies similar to a given movie.
        
        Args:
            movie_id: Reference movie ID
            limit: Number of similar movies
            
        Returns:
            List of (movie_id, similarity_score) tuples
        """
        try:
            if movie_id not in self.movie_ids:
                logger.warning(f"[ContentBased] Movie not found: {movie_id}")
                return []
            
            movie_idx = self.movie_ids.index(movie_id)
            similarities = self.movie_similarity_matrix[movie_idx]
            
            # Exclude the movie itself
            similarities[movie_idx] = -1
            
            top_indices = np.argsort(similarities)[-limit:][::-1]
            return [
                (self.movie_ids[i], float(similarities[i]))
                for i in top_indices
                if similarities[i] >= 0
            ]
        
        except Exception as e:
            logger.error(f"[ContentBased] Error getting similar movies: {str(e)}")
            return []
