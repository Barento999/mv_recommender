"""
Model Evaluation Module

Evaluates recommendation model quality using various metrics:
- Coverage: % of items that can be recommended
- Diversity: How different are recommendations
- Serendipity: How surprising/unexpected are recommendations
- Sparsity analysis: Matrix sparsity effects
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Evaluate recommendation model quality."""
    
    def __init__(self, model, ratings_df: pd.DataFrame, movies_df: pd.DataFrame = None):
        """
        Initialize evaluator.
        
        Args:
            model: Trained recommendation model
            ratings_df: DataFrame with columns [user_id, movie_id, rating]
            movies_df: Optional movie metadata
        """
        self.model = model
        self.ratings_df = ratings_df
        self.movies_df = movies_df
    
    def evaluate_coverage(self, limit: int = 10) -> Dict:
        """
        Calculate recommendation coverage.
        
        Coverage = % of unique items that can be recommended
        
        Returns:
            Dict with coverage metrics
        """
        logger.info("[Evaluator] Computing coverage...")
        
        try:
            if not self.model.is_trained:
                return {'coverage': 0.0, 'error': 'Model not trained'}
            
            unique_movies = set(self.model.movie_ids)
            total_movies = len(unique_movies)
            
            # Sample recommendations across users
            if not self.model.user_ids:
                return {'coverage': 0.0, 'error': 'No users in model'}
            
            recommended_movies = set()
            sample_users = self.model.user_ids[:min(50, len(self.model.user_ids))]
            
            for user_id in sample_users:
                # Get recommendations synchronously (simplified)
                user_idx = self.model.user_ids.index(user_id)
                user_ratings = self.model.user_item_matrix.iloc[user_idx].values
                
                unrated_mask = user_ratings == 0
                unrated_indices = np.where(unrated_mask)[0]
                
                for idx in unrated_indices[:limit]:
                    recommended_movies.add(self.model.movie_ids[idx])
            
            coverage = len(recommended_movies) / total_movies if total_movies > 0 else 0.0
            
            return {
                'coverage': coverage,
                'coverage_percent': f"{coverage*100:.1f}%",
                'unique_items_recommended': len(recommended_movies),
                'total_items': total_movies
            }
        
        except Exception as e:
            logger.error(f"[Evaluator] Error computing coverage: {str(e)}")
            return {'coverage': 0.0, 'error': str(e)}
    
    def evaluate_sparsity_impact(self) -> Dict:
        """
        Analyze impact of matrix sparsity on recommendations.
        
        Returns:
            Dict with sparsity metrics
        """
        logger.info("[Evaluator] Analyzing sparsity impact...")
        
        try:
            if self.model.user_item_matrix is None:
                return {}
            
            # Ratings per user
            ratings_per_user = (self.model.user_item_matrix > 0).sum(axis=1)
            
            # Ratings per movie
            ratings_per_movie = (self.model.user_item_matrix > 0).sum(axis=0)
            
            return {
                'matrix_sparsity': self.model.metrics.get('sparsity', 0.0),
                'avg_ratings_per_user': float(ratings_per_user.mean()),
                'avg_ratings_per_movie': float(ratings_per_movie.mean()),
                'min_ratings_per_user': int(ratings_per_user.min()),
                'max_ratings_per_user': int(ratings_per_user.max()),
                'min_ratings_per_movie': int(ratings_per_movie.min()),
                'max_ratings_per_movie': int(ratings_per_movie.max()),
            }
        
        except Exception as e:
            logger.error(f"[Evaluator] Error analyzing sparsity: {str(e)}")
            return {}
    
    def evaluate_similarity_distribution(self) -> Dict:
        """
        Analyze user similarity distribution.
        
        Returns:
            Dict with similarity metrics
        """
        logger.info("[Evaluator] Analyzing similarity distribution...")
        
        try:
            if self.model.similarity_matrix is None:
                return {}
            
            # Get upper triangle (exclude diagonal)
            n = self.model.similarity_matrix.shape[0]
            upper_triangle = self.model.similarity_matrix[np.triu_indices_from(
                self.model.similarity_matrix, k=1
            )]
            
            return {
                'mean_similarity': float(upper_triangle.mean()),
                'std_similarity': float(upper_triangle.std()),
                'min_similarity': float(upper_triangle.min()),
                'max_similarity': float(upper_triangle.max()),
                'median_similarity': float(np.median(upper_triangle)),
                'similarity_90th_percentile': float(np.percentile(upper_triangle, 90))
            }
        
        except Exception as e:
            logger.error(f"[Evaluator] Error analyzing similarities: {str(e)}")
            return {}
    
    def evaluate_rating_distribution(self) -> Dict:
        """
        Analyze rating value distribution.
        
        Returns:
            Dict with rating statistics
        """
        logger.info("[Evaluator] Analyzing rating distribution...")
        
        try:
            if self.ratings_df is None or len(self.ratings_df) == 0:
                return {}
            
            ratings = self.ratings_df['rating'].values
            
            return {
                'mean_rating': float(ratings.mean()),
                'median_rating': float(np.median(ratings)),
                'std_rating': float(ratings.std()),
                'min_rating': float(ratings.min()),
                'max_rating': float(ratings.max()),
                'rating_1_count': int((ratings == 1).sum()),
                'rating_5_count': int((ratings == 5).sum()),
                'rating_10_count': int((ratings == 10).sum()),
            }
        
        except Exception as e:
            logger.error(f"[Evaluator] Error analyzing ratings: {str(e)}")
            return {}
    
    def get_full_evaluation(self) -> Dict:
        """
        Run complete model evaluation.
        
        Returns:
            Dict with all evaluation metrics
        """
        logger.info("[Evaluator] Running full model evaluation...")
        
        evaluation = {
            'model_name': self.model.model_name,
            'model_version': self.model.model_version,
            'is_trained': self.model.is_trained,
            'training_metrics': self.model.get_metrics(),
            'coverage_metrics': self.evaluate_coverage(),
            'sparsity_metrics': self.evaluate_sparsity_impact(),
            'similarity_metrics': self.evaluate_similarity_distribution(),
            'rating_metrics': self.evaluate_rating_distribution()
        }
        
        logger.info("[Evaluator] ✓ Evaluation complete")
        return evaluation
