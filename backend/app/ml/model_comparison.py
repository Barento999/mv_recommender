"""
Model Comparison Framework

Compare multiple recommendation algorithms side-by-side.
Provides comprehensive evaluation and ranking.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)


class ModelComparison:
    """Compare multiple recommendation models."""
    
    def __init__(self):
        """Initialize model comparison."""
        self.models: Dict = {}
        self.results: Dict = {}
        self.comparison_timestamp: Optional[datetime] = None
    
    def register_model(self, name: str, model) -> None:
        """
        Register a model for comparison.
        
        Args:
            name: Model name identifier
            model: Model instance (must have train() and recommend() methods)
        """
        self.models[name] = model
        logger.info(f"[ModelComparison] Registered model: {name}")
    
    async def compare_on_test_set(self, test_users: List[str], 
                                  true_ratings: Dict[str, List[Tuple[str, float]]]) -> Dict:
        """
        Compare models on a test set of user preferences.
        
        Args:
            test_users: List of user IDs to test on
            true_ratings: Dict mapping user_id -> [(movie_id, rating), ...]
            
        Returns:
            Comparison results
        """
        logger.info(f"[ModelComparison] Comparing {len(self.models)} models on {len(test_users)} users...")
        
        results = {}
        
        for model_name, model in self.models.items():
            logger.info(f"[ModelComparison] Evaluating: {model_name}")
            
            model_results = {
                'model_name': model_name,
                'predictions': {},
                'metrics': {}
            }
            
            for user_id in test_users:
                try:
                    recommendations = await model.recommend(user_id, limit=10)
                    model_results['predictions'][user_id] = recommendations
                except Exception as e:
                    logger.warning(f"[ModelComparison] Error getting recommendations for {user_id}: {str(e)}")
                    model_results['predictions'][user_id] = []
            
            # Calculate metrics
            model_results['metrics'] = self._calculate_metrics(
                model_results['predictions'],
                true_ratings
            )
            
            results[model_name] = model_results
        
        self.results = results
        self.comparison_timestamp = datetime.now()
        
        return results
    
    def _calculate_metrics(self, predictions: Dict[str, List], 
                          true_ratings: Dict[str, List[Tuple[str, float]]]) -> Dict:
        """
        Calculate evaluation metrics for a model's predictions.
        
        Metrics:
        - Precision@k: % of recommendations that were rated >= 5.0
        - Recall@k: % of high-rated items that were recommended
        - NDCG: Normalized Discounted Cumulative Gain
        - Coverage: % of items recommended at least once
        
        Args:
            predictions: Model predictions
            true_ratings: Ground truth ratings
            
        Returns:
            Dict with metrics
        """
        try:
            precisions = []
            recalls = []
            ndcgs = []
            
            all_recommended = set()
            
            for user_id, recs in predictions.items():
                if user_id not in true_ratings or len(recs) == 0:
                    continue
                
                rec_movie_ids = [movie_id for movie_id, _ in recs]
                all_recommended.update(rec_movie_ids)
                
                # Get high-rated movies for this user
                true_high_rated = set()
                true_all_rated = set()
                
                for movie_id, rating in true_ratings[user_id]:
                    true_all_rated.add(movie_id)
                    if rating >= 5.0:
                        true_high_rated.add(movie_id)
                
                # Precision@k
                relevant = len(set(rec_movie_ids) & true_high_rated)
                precision = relevant / len(rec_movie_ids) if len(rec_movie_ids) > 0 else 0
                precisions.append(precision)
                
                # Recall@k
                recall = relevant / len(true_high_rated) if len(true_high_rated) > 0 else 0
                recalls.append(recall)
                
                # NDCG
                dcg = self._calculate_dcg(rec_movie_ids, true_high_rated)
                idcg = self._calculate_idcg(len(true_high_rated), len(rec_movie_ids))
                ndcg = dcg / idcg if idcg > 0 else 0
                ndcgs.append(ndcg)
            
            # Coverage
            total_items = len(set(
                movie_id 
                for user_recs in true_ratings.values() 
                for movie_id, _ in user_recs
            ))
            coverage = len(all_recommended) / total_items if total_items > 0 else 0
            
            return {
                'precision_at_10': float(np.mean(precisions)) if precisions else 0.0,
                'recall_at_10': float(np.mean(recalls)) if recalls else 0.0,
                'ndcg_at_10': float(np.mean(ndcgs)) if ndcgs else 0.0,
                'coverage': float(coverage),
                'n_evaluated': len(precisions),
            }
        
        except Exception as e:
            logger.error(f"[ModelComparison] Error calculating metrics: {str(e)}")
            return {}
    
    def _calculate_dcg(self, recommendations: List[str], relevant: set, k: int = 10) -> float:
        """Calculate Discounted Cumulative Gain."""
        dcg = 0.0
        for i, movie_id in enumerate(recommendations[:k]):
            if movie_id in relevant:
                dcg += 1.0 / np.log2(i + 2)  # +2 because log2(1) = 0
        return dcg
    
    def _calculate_idcg(self, n_relevant: int, k: int = 10) -> float:
        """Calculate Ideal DCG."""
        idcg = 0.0
        for i in range(min(n_relevant, k)):
            idcg += 1.0 / np.log2(i + 2)
        return idcg
    
    def rank_models(self, metric: str = 'ndcg_at_10') -> List[Tuple[str, float]]:
        """
        Rank models by a specific metric.
        
        Args:
            metric: Metric to rank by
            
        Returns:
            List of (model_name, score) sorted descending
        """
        if not self.results:
            logger.warning("[ModelComparison] No comparison results available")
            return []
        
        rankings = []
        for model_name, result in self.results.items():
            score = result['metrics'].get(metric, 0.0)
            rankings.append((model_name, score))
        
        rankings.sort(key=lambda x: x[1], reverse=True)
        
        logger.info("[ModelComparison] Model Rankings:")
        for i, (model_name, score) in enumerate(rankings, 1):
            logger.info(f"  {i}. {model_name}: {score:.4f}")
        
        return rankings
    
    def get_comparison_report(self) -> str:
        """Generate a comparison report."""
        if not self.results:
            return "No comparison results available"
        
        report = []
        report.append("="*70)
        report.append("MODEL COMPARISON REPORT")
        report.append("="*70)
        
        if self.comparison_timestamp:
            report.append(f"Generated: {self.comparison_timestamp.isoformat()}")
        
        report.append(f"\nModels compared: {len(self.results)}")
        report.append("")
        
        # Detailed results
        for model_name, result in self.results.items():
            report.append(f"\n{model_name}")
            report.append("-" * 40)
            
            metrics = result['metrics']
            for metric, value in metrics.items():
                if isinstance(value, float):
                    report.append(f"  {metric}: {value:.4f}")
                else:
                    report.append(f"  {metric}: {value}")
        
        # Rankings
        report.append("\n" + "="*70)
        report.append("RANKINGS (by NDCG@10)")
        report.append("="*70)
        
        rankings = self.rank_models('ndcg_at_10')
        for i, (model_name, score) in enumerate(rankings, 1):
            report.append(f"{i}. {model_name}: {score:.4f}")
        
        report.append("="*70)
        
        return "\n".join(report)
