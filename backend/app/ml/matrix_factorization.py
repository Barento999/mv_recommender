"""
Matrix Factorization Recommendation System

Implements SVD-based collaborative filtering.
Decomposes user-item matrix into latent factors.

Algorithm: Singular Value Decomposition (SVD)
- Reduces dimensionality
- Captures latent factors
- More scalable than user-user CF
"""

import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from typing import List, Tuple, Dict, Optional
import logging
import time

logger = logging.getLogger(__name__)


class MatrixFactorization:
    """SVD-based matrix factorization recommender."""
    
    def __init__(self, n_factors: int = 50, model_name: str = "matrix_factorization_v1"):
        """
        Initialize matrix factorization model.
        
        Args:
            n_factors: Number of latent factors (lower = faster, less accurate)
            model_name: Name for model versioning
        """
        self.n_factors = n_factors
        self.model_name = model_name
        self.model_version = "1.0.0"
        self.is_trained = False
        
        # Data
        self.user_item_matrix: Optional[pd.DataFrame] = None
        self.user_ids: Optional[List[str]] = None
        self.movie_ids: Optional[List[str]] = None
        
        # Latent factors
        self.U: Optional[np.ndarray] = None  # User factor matrix
        self.V: Optional[np.ndarray] = None  # Item factor matrix
        self.svd: Optional[TruncatedSVD] = None
        
        # Metrics
        self.metrics: Dict = {}
    
    def train(self, ratings_df: pd.DataFrame, movies_df: pd.DataFrame = None, 
              users_df: pd.DataFrame = None) -> bool:
        """
        Train matrix factorization model using SVD.
        
        Args:
            ratings_df: DataFrame with columns [user_id, movie_id, rating]
            movies_df: Optional movie metadata
            users_df: Optional user metadata
            
        Returns:
            True if training successful
        """
        start_time = time.time()
        
        try:
            logger.info("[MatrixFactorization] Training SVD model...")
            
            if ratings_df is None or len(ratings_df) == 0:
                logger.error("[MatrixFactorization] No ratings data")
                return False
            
            # Create user-item matrix
            pivot_table = ratings_df.pivot_table(
                index='user_id',
                columns='movie_id',
                values='rating',
                fill_value=0
            )
            
            self.user_item_matrix = pivot_table
            self.user_ids = pivot_table.index.tolist()
            self.movie_ids = pivot_table.columns.tolist()
            
            logger.info(f"[MatrixFactorization] Matrix shape: {pivot_table.shape}")
            
            # Apply SVD
            n_components = min(self.n_factors, min(pivot_table.shape) - 1)
            self.svd = TruncatedSVD(n_components=n_components, random_state=42)
            
            # Fit SVD
            transformed_data = self.svd.fit_transform(pivot_table.values)
            
            # Store factor matrices
            self.U = transformed_data  # User latent factors
            self.V = self.svd.components_.T  # Item latent factors
            
            self.is_trained = True
            training_time = time.time() - start_time
            
            # Calculate explained variance
            explained_variance = self.svd.explained_variance_ratio_.sum()
            
            self.metrics = {
                'model_name': self.model_name,
                'algorithm': 'Matrix Factorization (SVD)',
                'n_users': len(self.user_ids),
                'n_movies': len(self.movie_ids),
                'n_ratings': len(ratings_df),
                'n_factors': n_components,
                'explained_variance': float(explained_variance),
                'sparsity': 1.0 - (len(ratings_df) / (len(self.user_ids) * len(self.movie_ids))),
                'training_time_seconds': training_time,
                'trained_at': time.time()
            }
            
            logger.info(f"[MatrixFactorization] ✓ Training complete ({training_time:.3f}s)")
            logger.info(f"[MatrixFactorization] Factors: {n_components}, Explained variance: {explained_variance:.1%}")
            
            return True
        
        except Exception as e:
            logger.error(f"[MatrixFactorization] ✗ Training failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    async def recommend(self, user_id: str, limit: int = 10) -> List[Tuple[str, float]]:
        """
        Generate recommendations using latent factors.
        
        Args:
            user_id: User ID
            limit: Number of recommendations
            
        Returns:
            List of (movie_id, predicted_rating) tuples
        """
        try:
            if not self.is_trained:
                logger.warning("[MatrixFactorization] Model not trained")
                return []
            
            if user_id not in self.user_ids:
                logger.debug(f"[MatrixFactorization] Cold start for new user {user_id}")
                # Cold start: return popular movies
                avg_ratings = self.user_item_matrix.mean(axis=0)
                top_indices = np.argsort(avg_ratings.values)[-limit:][::-1]
                return [
                    (self.movie_ids[i], float(avg_ratings.iloc[i]))
                    for i in top_indices
                ]
            
            user_idx = self.user_ids.index(user_id)
            user_factors = self.U[user_idx]
            
            # Calculate predicted ratings
            predicted_ratings = np.dot(user_factors, self.V.T)
            
            # Get user's already-rated movies
            user_ratings = self.user_item_matrix.iloc[user_idx].values
            rated_mask = user_ratings > 0
            predicted_ratings[rated_mask] = -1  # Exclude already-rated
            
            # Get top recommendations
            top_indices = np.argsort(predicted_ratings)[-limit:][::-1]
            recommendations = [
                (self.movie_ids[i], float(max(1.0, min(10.0, predicted_ratings[i]))))
                for i in top_indices
                if predicted_ratings[i] >= 0
            ]
            
            return recommendations
        
        except Exception as e:
            logger.error(f"[MatrixFactorization] Error getting recommendations: {str(e)}")
            return []
    
    def get_metrics(self) -> Dict:
        """Return model metrics."""
        return self.metrics.copy()
    
    def get_user_factors(self, user_id: str) -> Optional[np.ndarray]:
        """Get latent factors for a user."""
        if user_id not in self.user_ids:
            return None
        user_idx = self.user_ids.index(user_id)
        return self.U[user_idx].copy()
    
    def get_item_factors(self, movie_id: str) -> Optional[np.ndarray]:
        """Get latent factors for an item."""
        if movie_id not in self.movie_ids:
            return None
        movie_idx = self.movie_ids.index(movie_id)
        return self.V[movie_idx].copy()
