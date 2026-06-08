"""
Collaborative Filtering Recommendation Model (Production ML Pipeline)

Architecture:
1. MLModel: Core model class (abstract base for different algorithms)
2. UserUserCF: User-User Collaborative Filtering (current implementation)
3. ModelTrainer: Handles model training from CSV/DataFrame
4. ModelEvaluator: Evaluates model quality metrics
5. ModelRegistry: Manages model persistence and versioning

Data Flow:
CSV → DataLoader → DataFrames → ModelTrainer → Trained Model → Predictions

Features:
- Modular design (easily swap algorithms)
- Model persistence (save/load from disk)
- Training metrics and monitoring
- Incremental updates
- Production error handling
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Dict, Optional, Any
from abc import ABC, abstractmethod
from pathlib import Path
import pickle
import json
import time
import logging

logger = logging.getLogger(__name__)


# For backward compatibility with existing code
try:
    from app.database import get_database
except ImportError:
    get_database = None


class MLModel(ABC):
    """Abstract base class for ML recommendation models."""
    
    @abstractmethod
    def train(self, ratings_df: pd.DataFrame, movies_df: pd.DataFrame = None, users_df: pd.DataFrame = None) -> bool:
        """Train the model on provided data."""
        pass
    
    @abstractmethod
    async def recommend(self, user_id: str, limit: int = 10) -> List[Tuple[str, float]]:
        """Generate recommendations for a user."""
        pass
    
    @abstractmethod
    def get_metrics(self) -> Dict:
        """Get model metrics and statistics."""
        pass


class UserUserCollaborativeFiltering(MLModel):
    """
    Production User-User Collaborative Filtering Model
    
    Implements best practices for production ML:
    - Modular design
    - Training/inference separation
    - Metrics tracking
    - Error handling with logging
    - Model persistence support
    """
    
    def __init__(self, k_neighbors: int = 10, model_name: str = "user_user_cf_v1"):
        """
        Initialize the model.
        
        Args:
            k_neighbors: Number of neighbors to consider
            model_name: Name for model versioning
        """
        self.k_neighbors = k_neighbors
        self.model_name = model_name
        self.model_version = "1.0.0"
        
        # Model state
        self.is_trained = False
        self.user_item_matrix: Optional[pd.DataFrame] = None
        self.user_ids: Optional[List[str]] = None
        self.movie_ids: Optional[List[str]] = None
        self.similarity_matrix: Optional[np.ndarray] = None
        
        # Metadata
        self.trained_at: Optional[float] = None
        self.training_time: float = 0.0
        self.metrics: Dict = {}
    
    def train(self, ratings_df: pd.DataFrame, movies_df: pd.DataFrame = None, users_df: pd.DataFrame = None) -> bool:
        """
        Train the collaborative filtering model.
        
        Args:
            ratings_df: DataFrame with columns [user_id, movie_id, rating]
            movies_df: Optional movie metadata
            users_df: Optional user metadata
            
        Returns:
            True if training successful, False otherwise
        """
        logger.info(f"[{self.model_name}] Starting training...")
        start_time = time.time()
        
        try:
            # Validate input
            if ratings_df is None or len(ratings_df) == 0:
                logger.warning(f"[{self.model_name}] ⚠️  No ratings provided for training")
                return False
            
            required_cols = ['user_id', 'movie_id', 'rating']
            if not all(col in ratings_df.columns for col in required_cols):
                logger.error(f"[{self.model_name}] ✗ Missing required columns: {required_cols}")
                return False
            
            # Build user-item matrix
            logger.debug(f"[{self.model_name}] Building user-item matrix...")
            self.user_item_matrix = ratings_df.pivot_table(
                index='user_id',
                columns='movie_id',
                values='rating',
                fill_value=0.0
            )
            
            self.user_ids = self.user_item_matrix.index.tolist()
            self.movie_ids = self.user_item_matrix.columns.tolist()
            
            n_users = len(self.user_ids)
            n_movies = len(self.movie_ids)
            n_ratings = len(ratings_df)
            
            # Validate minimum data
            if n_users < 2 or n_movies < 2:
                logger.warning(f"[{self.model_name}] ⚠️  Insufficient data: {n_users} users, {n_movies} movies")
                return False
            
            # Compute similarity
            logger.debug(f"[{self.model_name}] Computing user-user similarity...")
            self.similarity_matrix = cosine_similarity(self.user_item_matrix)
            
            # Calculate metrics
            self.training_time = time.time() - start_time
            self.trained_at = time.time()
            self.is_trained = True
            
            self.metrics = {
                'n_users': n_users,
                'n_movies': n_movies,
                'n_ratings': n_ratings,
                'sparsity': 1 - (n_ratings / (n_users * n_movies)),
                'training_time_seconds': self.training_time,
                'model_version': self.model_version,
                'algorithm': 'user_user_cf'
            }
            
            logger.info(f"[{self.model_name}] ✓ Training complete in {self.training_time:.3f}s")
            logger.info(f"[{self.model_name}]   • Users: {n_users} | Movies: {n_movies} | Ratings: {n_ratings}")
            logger.info(f"[{self.model_name}]   • Sparsity: {self.metrics['sparsity']:.1%}")
            
            return True
            
        except Exception as e:
            logger.error(f"[{self.model_name}] ✗ Training failed: {str(e)}")
            self.is_trained = False
            return False
    
    async def recommend(self, user_id: str, limit: int = 10) -> List[Tuple[str, float]]:
        """
        Generate recommendations for a user.
        
        Args:
            user_id: The user to recommend for
            limit: Number of recommendations
            
        Returns:
            List of (movie_id, predicted_score) tuples
        """
        if not self.is_trained or self.user_item_matrix is None:
            logger.warning(f"[{self.model_name}] Model not trained")
            return []
        
        try:
            if user_id not in self.user_ids:
                logger.debug(f"[{self.model_name}] Cold start: user {user_id} not in training data")
                return await self._get_top_rated(limit)
            
            user_idx = self.user_ids.index(user_id)
            user_ratings = self.user_item_matrix.iloc[user_idx].values
            
            # Get similar users
            similarities = self.similarity_matrix[user_idx]
            similar_indices = np.argsort(similarities)[::-1][1:self.k_neighbors+1]
            similar_indices = [idx for idx in similar_indices if similarities[idx] > 0]
            
            if not similar_indices:
                return await self._get_top_rated(limit)
            
            # Predict ratings for unrated movies
            predicted_ratings = np.zeros(len(self.movie_ids))
            similarity_weights = np.zeros(len(self.movie_ids))
            
            for idx in similar_indices:
                sim_score = similarities[idx]
                neighbor_ratings = self.user_item_matrix.iloc[idx].values
                
                predicted_ratings += sim_score * neighbor_ratings
                similarity_weights += sim_score * (neighbor_ratings > 0)
            
            predicted_ratings = np.divide(
                predicted_ratings,
                similarity_weights,
                where=similarity_weights > 0,
                out=np.zeros_like(predicted_ratings)
            )
            
            # Get unrated movies
            unrated_mask = user_ratings == 0
            unrated_indices = np.where(unrated_mask)[0]
            
            recommendations = [
                (self.movie_ids[idx], float(predicted_ratings[idx]))
                for idx in unrated_indices
                if predicted_ratings[idx] > 0
            ]
            
            recommendations.sort(key=lambda x: x[1], reverse=True)
            return recommendations[:limit]
            
        except Exception as e:
            logger.error(f"[{self.model_name}] Error generating recommendations: {str(e)}")
            return await self._get_top_rated(limit)
    
    async def _get_top_rated(self, limit: int) -> List[Tuple[str, float]]:
        """Fallback: return top-rated movies."""
        if self.user_item_matrix is None:
            return []
        
        avg_ratings = (self.user_item_matrix.sum(axis=0)) / (self.user_item_matrix > 0).sum(axis=0)
        top_movies = avg_ratings.nlargest(limit)
        return [(str(mid), float(rating)) for mid, rating in top_movies.items()]
    
    def get_metrics(self) -> Dict:
        """Get model metrics."""
        return self.metrics.copy()
    
    def save(self, filepath: str) -> bool:
        """Save model to disk."""
        try:
            model_data = {
                'user_ids': self.user_ids,
                'movie_ids': self.movie_ids,
                'similarity_matrix': self.similarity_matrix,
                'metrics': self.metrics,
                'k_neighbors': self.k_neighbors,
                'model_name': self.model_name,
            }
            
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info(f"[{self.model_name}] ✓ Model saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"[{self.model_name}] ✗ Error saving model: {str(e)}")
            return False
    
    def load(self, filepath: str) -> bool:
        """Load model from disk."""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.user_ids = model_data['user_ids']
            self.movie_ids = model_data['movie_ids']
            self.similarity_matrix = model_data['similarity_matrix']
            self.metrics = model_data['metrics']
            self.k_neighbors = model_data.get('k_neighbors', 10)
            self.is_trained = True
            
            logger.info(f"[{self.model_name}] ✓ Model loaded from {filepath}")
            return True
        except Exception as e:
            logger.error(f"[{self.model_name}] ✗ Error loading model: {str(e)}")
            return False


# Legacy class for backward compatibility
class CollaborativeFilteringModel(UserUserCollaborativeFiltering):
    """Backward compatibility wrapper for existing code."""
    
    def __init__(self, k_neighbors: int = 10, min_common_ratings: int = 2):
        super().__init__(k_neighbors=k_neighbors, model_name="collaborative_filtering")
        self.min_common_ratings = min_common_ratings

    async def build_model(self) -> bool:
        """
        Build the user-item rating matrix and compute similarities.
        
        For backward compatibility - loads from database and trains.
        """
        try:
            if get_database is None:
                logger.error("[Legacy] Database not available")
                return False
            
            db = get_database()
            ratings_cursor = await db.ratings.find({}).to_list(None)
            
            if not ratings_cursor:
                logger.warning("[Legacy] No ratings in database")
                return False
            
            ratings_data = []
            for rating in ratings_cursor:
                ratings_data.append({
                    'user_id': str(rating['user_id']),
                    'movie_id': str(rating['movie_id']),
                    'rating': float(rating['rating'])
                })
            
            ratings_df = pd.DataFrame(ratings_data)
            return self.train(ratings_df)
            
        except Exception as e:
            logger.error(f"[Legacy] Error building model: {str(e)}")
            return False

    def get_similar_users(self, user_id: str, k: Optional[int] = None) -> List[Tuple[str, float]]:
        """Find k most similar users (legacy method)."""
        if self.similarity_matrix is None or self.user_item_matrix is None:
            return []
        
        if user_id not in self.user_ids:
            return []
        
        k = k or self.k_neighbors
        user_idx = self.user_ids.index(user_id)
        similarities = self.similarity_matrix[user_idx]
        similar_indices = np.argsort(similarities)[::-1][1:k+1]
        
        return [
            (self.user_ids[idx], float(similarities[idx]))
            for idx in similar_indices
            if similarities[idx] > 0
        ]

    async def recommend_movies(
        self,
        user_id: str,
        limit: int = 10,
        exclude_rated: bool = True
    ) -> List[Tuple[str, float]]:
        """Legacy recommend_movies method."""
        return await self.recommend(user_id, limit)

    async def _get_top_rated_movies(self, limit: int) -> List[Tuple[str, float]]:
        """Legacy fallback method."""
        return await self._get_top_rated(limit)

    def get_model_stats(self) -> Dict:
        """Legacy stats method."""
        return self.get_metrics()


# Global model instance (singleton)
_model_instance: Optional[UserUserCollaborativeFiltering] = None


async def get_model() -> UserUserCollaborativeFiltering:
    """Get or create the global model instance."""
    global _model_instance
    if _model_instance is None:
        _model_instance = UserUserCollaborativeFiltering()
        # Try to build from database for backward compatibility
        await _model_instance.build_model()
    return _model_instance


async def rebuild_model() -> bool:
    """Rebuild the model from database."""
    global _model_instance
    _model_instance = UserUserCollaborativeFiltering()
    return await _model_instance.build_model()


def get_model_stats() -> Dict:
    """Get current model statistics."""
    global _model_instance
    if _model_instance is None:
        return {}
    return _model_instance.get_metrics()


# New production functions for CSV-based pipeline

def create_model_from_csv(
    ratings_csv: str,
    movies_csv: str = None,
    users_csv: str = None,
    k_neighbors: int = 10
) -> Optional[UserUserCollaborativeFiltering]:
    """
    Create and train a model from CSV files.
    
    Args:
        ratings_csv: Path to ratings CSV
        movies_csv: Optional path to movies CSV
        users_csv: Optional path to users CSV
        k_neighbors: Number of neighbors for CF
        
    Returns:
        Trained model or None if failed
    """
    try:
        from app.ml.data_loader import DataLoader
        
        logger.info("[MLPipeline] Creating model from CSV files...")
        
        # Load data
        loader = DataLoader()
        ratings_df = loader.load_ratings(ratings_csv)
        movies_df = loader.load_movies(movies_csv) if movies_csv else None
        users_df = loader.load_users(users_csv) if users_csv else None
        
        # Create and train model
        model = UserUserCollaborativeFiltering(k_neighbors=k_neighbors)
        success = model.train(ratings_df, movies_df, users_df)
        
        if success:
            logger.info("[MLPipeline] ✓ Model created successfully from CSV")
            return model
        else:
            logger.error("[MLPipeline] ✗ Failed to train model from CSV")
            return None
            
    except Exception as e:
        logger.error(f"[MLPipeline] ✗ Error creating model from CSV: {str(e)}")
        return None


def set_global_model(model: UserUserCollaborativeFiltering):
    """Set the global model instance."""
    global _model_instance
    _model_instance = model
    logger.info("[MLPipeline] Global model updated")
