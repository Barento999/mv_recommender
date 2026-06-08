"""
Recommendation Blending & Ensemble Methods

Combines predictions from multiple models to improve recommendation quality.
Implements several blending strategies.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import logging
import asyncio

logger = logging.getLogger(__name__)


class RecommendationBlender:
    """Blend recommendations from multiple models."""
    
    def __init__(self, blend_method: str = 'weighted_average'):
        """
        Initialize recommender blender.
        
        Args:
            blend_method: 'weighted_average', 'linear_combination', 'voting', 'stacking'
        """
        self.blend_method = blend_method
        self.models: Dict = {}
        self.weights: Dict[str, float] = {}
        self.predictions_cache: Dict = {}
    
    def add_model(self, name: str, model, weight: float = 1.0) -> None:
        """
        Add a model to the ensemble.
        
        Args:
            name: Model name
            model: Model instance
            weight: Weight for blending (higher = more influence)
        """
        self.models[name] = model
        self.weights[name] = weight
        logger.info(f"[Blender] Added model: {name} (weight={weight})")
    
    def normalize_weights(self) -> None:
        """Normalize weights to sum to 1.0."""
        total = sum(self.weights.values())
        if total > 0:
            for name in self.weights:
                self.weights[name] /= total
        logger.info(f"[Blender] Normalized weights: {self.weights}")
    
    async def blend_recommendations(self, user_id: str, limit: int = 10) -> List[Tuple[str, float]]:
        """
        Get blended recommendations from multiple models.
        
        Args:
            user_id: User ID
            limit: Number of recommendations
            
        Returns:
            List of (movie_id, blended_score) tuples
        """
        if not self.models:
            logger.warning("[Blender] No models registered")
            return []
        
        logger.debug(f"[Blender] Blending recommendations for {user_id}...")
        
        try:
            # Get predictions from all models
            all_predictions = {}
            
            for model_name, model in self.models.items():
                try:
                    recommendations = await model.recommend(user_id, limit=limit * 2)
                    all_predictions[model_name] = {
                        movie_id: score 
                        for movie_id, score in recommendations
                    }
                except Exception as e:
                    logger.warning(f"[Blender] Error from {model_name}: {str(e)}")
                    all_predictions[model_name] = {}
            
            # Blend predictions
            if self.blend_method == 'weighted_average':
                blended = self._blend_weighted_average(all_predictions)
            elif self.blend_method == 'voting':
                blended = self._blend_voting(all_predictions)
            else:
                blended = self._blend_weighted_average(all_predictions)  # Default
            
            # Sort by score and return top-k
            sorted_recs = sorted(blended.items(), key=lambda x: x[1], reverse=True)
            
            return sorted_recs[:limit]
        
        except Exception as e:
            logger.error(f"[Blender] Error blending recommendations: {str(e)}")
            return []
    
    def _blend_weighted_average(self, predictions: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Blend using weighted average of scores.
        
        Args:
            predictions: Dict[model_name -> Dict[movie_id -> score]]
            
        Returns:
            Dict[movie_id -> blended_score]
        """
        blended = {}
        
        # Normalize weights
        self.normalize_weights()
        
        # Collect all movie IDs
        all_movies = set()
        for model_preds in predictions.values():
            all_movies.update(model_preds.keys())
        
        # Calculate weighted average for each movie
        for movie_id in all_movies:
            weighted_sum = 0.0
            weight_sum = 0.0
            
            for model_name, model_preds in predictions.items():
                if movie_id in model_preds:
                    score = model_preds[movie_id]
                    weight = self.weights.get(model_name, 1.0)
                    weighted_sum += score * weight
                    weight_sum += weight
            
            if weight_sum > 0:
                blended[movie_id] = weighted_sum / weight_sum
        
        return blended
    
    def _blend_voting(self, predictions: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Blend using voting (majority vote on whether to recommend).
        
        Args:
            predictions: Dict[model_name -> Dict[movie_id -> score]]
            
        Returns:
            Dict[movie_id -> confidence_score]
        """
        blended = {}
        n_models = len(predictions)
        
        # Collect all movie IDs
        all_movies = set()
        for model_preds in predictions.values():
            all_movies.update(model_preds.keys())
        
        # Calculate voting score
        for movie_id in all_movies:
            votes = 0
            total_score = 0.0
            
            for model_preds in predictions.values():
                if movie_id in model_preds:
                    votes += 1
                    total_score += model_preds[movie_id]
            
            # Confidence: (votes / n_models) * (avg_score / 10)
            vote_confidence = votes / n_models if n_models > 0 else 0
            score_confidence = (total_score / votes) / 10.0 if votes > 0 else 0
            
            blended[movie_id] = (vote_confidence + score_confidence) / 2
        
        return blended
    
    def _blend_linear_combination(self, predictions: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Blend using linear combination with learned weights.
        
        Args:
            predictions: Dict[model_name -> Dict[movie_id -> score]]
            
        Returns:
            Dict[movie_id -> blended_score]
        """
        # Similar to weighted average but with optional learning
        return self._blend_weighted_average(predictions)
    
    def evaluate_blend_quality(self, test_recommendations: List[Tuple[str, List[Tuple[str, float]]]], 
                              true_ratings: Dict[str, float]) -> Dict:
        """
        Evaluate quality of blended recommendations.
        
        Args:
            test_recommendations: List of (user_id, [(movie_id, score), ...])
            true_ratings: Dict mapping movie_id -> actual_rating
            
        Returns:
            Evaluation metrics
        """
        try:
            correct = 0
            total = 0
            
            for user_id, recommendations in test_recommendations:
                for movie_id, predicted_score in recommendations:
                    if movie_id in true_ratings:
                        actual_rating = true_ratings[movie_id]
                        
                        # Calculate error
                        error = abs(predicted_score - actual_rating)
                        if error < 2.0:  # Close enough
                            correct += 1
                        total += 1
            
            accuracy = correct / total if total > 0 else 0
            
            return {
                'accuracy': accuracy,
                'n_evaluated': total,
                'blend_method': self.blend_method,
            }
        
        except Exception as e:
            logger.error(f"[Blender] Error evaluating blend quality: {str(e)}")
            return {}
