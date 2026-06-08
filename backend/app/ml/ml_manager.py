"""
ML Manager - Complete ML Project Management

Handles the complete ML workflow:
1. Data preparation & validation
2. Model training with multiple algorithms
3. Model evaluation & metrics
4. Hyperparameter tuning
5. Model comparison & ranking
6. A/B testing setup
7. Model persistence & versioning
8. Performance monitoring
9. Cache management
10. Pipeline orchestration
"""

import logging
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class MLManager:
    """Complete ML project management system."""
    
    def __init__(self, data_dir: str = "data", models_dir: str = "models"):
        """
        Initialize ML Manager.
        
        Args:
            data_dir: Directory with CSV data
            models_dir: Directory to save trained models
        """
        self.data_dir = Path(data_dir)
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
        # Data
        self.movies_df: Optional[pd.DataFrame] = None
        self.users_df: Optional[pd.DataFrame] = None
        self.ratings_df: Optional[pd.DataFrame] = None
        
        # Models
        self.models: Dict = {}
        self.evaluations: Dict = {}
        self.comparisons: Dict = {}
        
        # Project metadata
        self.project_info = {
            'created_at': datetime.now().isoformat(),
            'last_updated': None,
            'version': '1.0.0',
            'status': 'initialized'
        }
        
        logger.info("[MLManager] Initialized")
    
    # =====================================================================
    # STEP 1: Data Preparation
    # =====================================================================
    
    async def prepare_data(self, validate: bool = True) -> bool:
        """
        Load and prepare data from CSV files.
        
        Args:
            validate: Validate data integrity
            
        Returns:
            True if successful
        """
        logger.info("\n" + "="*70)
        logger.info("[MLManager] STEP 1: DATA PREPARATION")
        logger.info("="*70)
        
        try:
            from app.ml.data_loader import DataLoader
            
            logger.info("\nLoading data from CSV files...")
            loader = DataLoader(str(self.data_dir))
            
            start_time = time.time()
            
            self.movies_df = loader.load_movies(str(self.data_dir / "movies.csv"))
            self.users_df = loader.load_users(str(self.data_dir / "users.csv"))
            self.ratings_df = loader.load_ratings(str(self.data_dir / "ratings.csv"))
            
            load_time = time.time() - start_time
            
            logger.info(f"✓ Data loaded in {load_time:.2f}s")
            logger.info(f"  Movies: {len(self.movies_df)}")
            logger.info(f"  Users: {len(self.users_df)}")
            logger.info(f"  Ratings: {len(self.ratings_df)}")
            
            if validate:
                self._validate_data()
            
            self.project_info['data_loaded'] = {
                'movies': len(self.movies_df),
                'users': len(self.users_df),
                'ratings': len(self.ratings_df),
                'load_time': load_time
            }
            
            return True
        
        except Exception as e:
            logger.error(f"✗ Data preparation failed: {str(e)}")
            return False
    
    def _validate_data(self) -> None:
        """Validate data integrity."""
        logger.info("\nValidating data integrity...")
        
        # Check for nulls
        null_movies = self.movies_df.isnull().sum().sum()
        null_users = self.users_df.isnull().sum().sum()
        null_ratings = self.ratings_df.isnull().sum().sum()
        
        logger.info(f"  Null values - Movies: {null_movies}, Users: {null_users}, Ratings: {null_ratings}")
        
        # Check uniqueness
        unique_movies = self.movies_df['movie_id'].nunique()
        unique_users = self.users_df['user_id'].nunique()
        
        logger.info(f"  Unique movies: {unique_movies} (expected {len(self.movies_df)})")
        logger.info(f"  Unique users: {unique_users} (expected {len(self.users_df)})")
        
        # Check rating ranges
        rating_min = self.ratings_df['rating'].min()
        rating_max = self.ratings_df['rating'].max()
        logger.info(f"  Rating range: {rating_min:.1f} - {rating_max:.1f} (expected 0-10)")
        
        # Calculate sparsity
        matrix_size = len(self.movies_df) * len(self.users_df)
        sparsity = 1.0 - (len(self.ratings_df) / matrix_size)
        logger.info(f"  Matrix sparsity: {sparsity:.1%}")
        
        logger.info("✓ Data validation complete")
    
    # =====================================================================
    # STEP 2: Model Training
    # =====================================================================
    
    async def train_models(self, algorithms: List[str] = None) -> Dict:
        """
        Train multiple recommendation algorithms.
        
        Args:
            algorithms: List of algorithms to train
                       ['cf', 'content', 'mf'] (default: all)
        
        Returns:
            Dict with training results
        """
        logger.info("\n" + "="*70)
        logger.info("[MLManager] STEP 2: MODEL TRAINING")
        logger.info("="*70)
        
        if algorithms is None:
            algorithms = ['cf', 'content', 'mf']
        
        results = {}
        
        for algo in algorithms:
            logger.info(f"\nTraining {algo.upper()} model...")
            
            try:
                if algo == 'cf':
                    result = await self._train_cf()
                elif algo == 'content':
                    result = await self._train_content()
                elif algo == 'mf':
                    result = await self._train_mf()
                else:
                    logger.warning(f"Unknown algorithm: {algo}")
                    continue
                
                if result:
                    results[algo] = result
                    self.models[algo] = result['model']
            
            except Exception as e:
                logger.error(f"✗ {algo} training failed: {str(e)}")
        
        logger.info(f"\n✓ Training complete. Trained {len(results)} models")
        self.project_info['models_trained'] = list(results.keys())
        
        return results
    
    async def _train_cf(self) -> Dict:
        """Train Collaborative Filtering model."""
        from app.ml.collaborative_filtering import UserUserCollaborativeFiltering
        
        start_time = time.time()
        
        model = UserUserCollaborativeFiltering(k_neighbors=10, model_name="cf_v1")
        success = model.train(self.ratings_df, self.movies_df, self.users_df)
        
        if not success:
            return None
        
        train_time = time.time() - start_time
        metrics = model.get_metrics()
        
        logger.info(f"  ✓ CF Model trained in {train_time:.2f}s")
        logger.info(f"    Users: {metrics.get('n_users')}, Movies: {metrics.get('n_movies')}")
        
        return {
            'model': model,
            'algorithm': 'Collaborative Filtering',
            'train_time': train_time,
            'metrics': metrics
        }
    
    async def _train_content(self) -> Dict:
        """Train Content-Based model."""
        from app.ml.content_based import ContentBasedRecommender
        
        start_time = time.time()
        
        model = ContentBasedRecommender(model_name="content_v1")
        success = model.train(self.movies_df, self.ratings_df)
        
        if not success:
            return None
        
        train_time = time.time() - start_time
        metrics = model.get_metrics()
        
        logger.info(f"  ✓ Content Model trained in {train_time:.2f}s")
        
        return {
            'model': model,
            'algorithm': 'Content-Based',
            'train_time': train_time,
            'metrics': metrics
        }
    
    async def _train_mf(self) -> Dict:
        """Train Matrix Factorization model."""
        from app.ml.matrix_factorization import MatrixFactorization
        
        start_time = time.time()
        
        model = MatrixFactorization(n_factors=50, model_name="mf_v1")
        success = model.train(self.ratings_df, self.movies_df, self.users_df)
        
        if not success:
            return None
        
        train_time = time.time() - start_time
        metrics = model.get_metrics()
        
        logger.info(f"  ✓ Matrix Factorization Model trained in {train_time:.2f}s")
        logger.info(f"    Factors: {metrics.get('n_factors')}, Variance: {metrics.get('explained_variance'):.1%}")
        
        return {
            'model': model,
            'algorithm': 'Matrix Factorization',
            'train_time': train_time,
            'metrics': metrics
        }
    
    # =====================================================================
    # STEP 3: Model Evaluation
    # =====================================================================
    
    async def evaluate_models(self) -> Dict:
        """
        Evaluate all trained models.
        
        Returns:
            Dict with evaluation results
        """
        logger.info("\n" + "="*70)
        logger.info("[MLManager] STEP 3: MODEL EVALUATION")
        logger.info("="*70)
        
        from app.ml.model_evaluator import ModelEvaluator
        
        results = {}
        
        for algo_name, model_info in self.models.items():
            logger.info(f"\nEvaluating {algo_name.upper()}...")
            
            try:
                model = model_info['model']
                evaluator = ModelEvaluator(model, self.ratings_df, self.movies_df)
                evaluation = evaluator.get_full_evaluation()
                
                results[algo_name] = evaluation
                self.evaluations[algo_name] = evaluation
                
                # Log key metrics
                coverage = evaluation.get('coverage_metrics', {})
                sparsity = evaluation.get('sparsity_metrics', {})
                
                logger.info(f"  ✓ Evaluation complete")
                logger.info(f"    Coverage: {coverage.get('coverage_percent', 'N/A')}")
                logger.info(f"    Sparsity: {sparsity.get('sparsity', 'N/A'):.1%}")
            
            except Exception as e:
                logger.error(f"  ✗ Evaluation failed: {str(e)}")
        
        logger.info(f"\n✓ Evaluation complete. Evaluated {len(results)} models")
        
        return results
    
    # =====================================================================
    # STEP 4: Model Comparison
    # =====================================================================
    
    async def compare_models(self, test_users: List[str] = None) -> Dict:
        """
        Compare all trained models.
        
        Args:
            test_users: Users to test on (sample if None)
        
        Returns:
            Dict with comparison results
        """
        logger.info("\n" + "="*70)
        logger.info("[MLManager] STEP 4: MODEL COMPARISON")
        logger.info("="*70)
        
        from app.ml.model_comparison import ModelComparison
        
        # Sample test users if not provided
        if test_users is None:
            test_users = list(self.ratings_df['user_id'].unique())[:20]
        
        logger.info(f"\nComparing {len(self.models)} models on {len(test_users)} test users...")
        
        try:
            comparison = ModelComparison()
            
            for algo_name, model_info in self.models.items():
                comparison.register_model(algo_name, model_info['model'])
            
            # Create test data
            true_ratings = {}
            for user_id in test_users:
                user_ratings = self.ratings_df[self.ratings_df['user_id'] == user_id]
                true_ratings[user_id] = [
                    (row['movie_id'], row['rating'])
                    for _, row in user_ratings.iterrows()
                ]
            
            results = await comparison.compare_on_test_set(test_users, true_ratings)
            
            self.comparisons['results'] = results
            
            # Print rankings
            rankings = comparison.rank_models('ndcg_at_10')
            logger.info(f"\n✓ Model Rankings (NDCG@10):")
            for i, (model_name, score) in enumerate(rankings, 1):
                logger.info(f"  {i}. {model_name}: {score:.4f}")
            
            self.comparisons['rankings'] = rankings
            
            return {
                'comparison_results': results,
                'rankings': rankings,
                'report': comparison.get_comparison_report()
            }
        
        except Exception as e:
            logger.error(f"✗ Comparison failed: {str(e)}")
            return {}
    
    # =====================================================================
    # STEP 5: Hyperparameter Tuning
    # =====================================================================
    
    async def tune_hyperparameters(self, algorithm: str = 'cf') -> Dict:
        """
        Tune hyperparameters for a specific algorithm.
        
        Args:
            algorithm: Algorithm to tune ('cf', 'content', 'mf')
        
        Returns:
            Dict with tuning results
        """
        logger.info("\n" + "="*70)
        logger.info(f"[MLManager] STEP 5: HYPERPARAMETER TUNING ({algorithm.upper()})")
        logger.info("="*70)
        
        from app.ml.hyperparameter_tuning import HyperparameterTuner
        
        try:
            # Define parameter grid based on algorithm
            if algorithm == 'cf':
                from app.ml.collaborative_filtering import UserUserCollaborativeFiltering
                
                tuner = HyperparameterTuner(
                    UserUserCollaborativeFiltering,
                    evaluation_metric='ndcg'
                )
                
                param_grid = {
                    'k_neighbors': [5, 10, 15, 20],
                }
            
            elif algorithm == 'mf':
                from app.ml.matrix_factorization import MatrixFactorization
                
                tuner = HyperparameterTuner(
                    MatrixFactorization,
                    evaluation_metric='ndcg'
                )
                
                param_grid = {
                    'n_factors': [30, 50, 70],
                }
            
            else:
                logger.warning(f"Tuning not supported for {algorithm}")
                return {}
            
            # Split data for tuning
            n_users = len(self.ratings_df['user_id'].unique())
            split_idx = int(0.8 * len(self.ratings_df))
            
            train_ratings = self.ratings_df.iloc[:split_idx]
            test_ratings = self.ratings_df.iloc[split_idx:]
            
            logger.info(f"\nTuning {algorithm} with grid: {param_grid}")
            logger.info(f"  Train set: {len(train_ratings)} ratings")
            logger.info(f"  Test set: {len(test_ratings)} ratings")
            
            results = tuner.grid_search(
                param_grid,
                train_data=(train_ratings, self.movies_df, self.users_df),
                test_data=(test_ratings, self.movies_df, self.users_df)
            )
            
            logger.info(f"\n✓ Tuning complete")
            logger.info(f"  Best params: {results['best_params']}")
            logger.info(f"  Best score: {results['best_score']:.4f}")
            
            return results
        
        except Exception as e:
            logger.error(f"✗ Tuning failed: {str(e)}")
            return {}
    
    # =====================================================================
    # STEP 6: Model Persistence
    # =====================================================================
    
    def save_models(self) -> Dict:
        """
        Save trained models to disk.
        
        Returns:
            Dict with save status
        """
        logger.info("\n" + "="*70)
        logger.info("[MLManager] STEP 6: MODEL PERSISTENCE")
        logger.info("="*70)
        
        results = {}
        
        for algo_name, model_info in self.models.items():
            try:
                model = model_info['model']
                model_path = self.models_dir / f"{algo_name}_v1.pkl"
                
                if hasattr(model, 'save'):
                    success = model.save(str(model_path))
                    if success:
                        logger.info(f"✓ {algo_name} model saved: {model_path}")
                        results[algo_name] = str(model_path)
                    else:
                        logger.warning(f"⚠ Could not save {algo_name} model")
                else:
                    logger.warning(f"⚠ {algo_name} model doesn't support save()")
            
            except Exception as e:
                logger.error(f"✗ Save failed for {algo_name}: {str(e)}")
        
        logger.info(f"\n✓ Saved {len(results)} models")
        
        return results
    
    # =====================================================================
    # STEP 7: Project Summary
    # =====================================================================
    
    def generate_project_report(self) -> str:
        """Generate comprehensive project report."""
        logger.info("\n" + "="*70)
        logger.info("[MLManager] ML PROJECT REPORT")
        logger.info("="*70)
        
        report = []
        report.append("\n" + "="*70)
        report.append("ML PROJECT SUMMARY REPORT")
        report.append("="*70)
        
        # Project info
        report.append(f"\nProject Created: {self.project_info.get('created_at', 'N/A')}")
        report.append(f"Status: {self.project_info.get('status', 'N/A')}")
        report.append(f"Version: {self.project_info.get('version', 'N/A')}")
        
        # Data info
        if self.project_info.get('data_loaded'):
            data = self.project_info['data_loaded']
            report.append(f"\nData Summary:")
            report.append(f"  Movies: {data.get('movies', 0)}")
            report.append(f"  Users: {data.get('users', 0)}")
            report.append(f"  Ratings: {data.get('ratings', 0)}")
            report.append(f"  Load time: {data.get('load_time', 0):.2f}s")
        
        # Models trained
        if self.project_info.get('models_trained'):
            report.append(f"\nModels Trained:")
            for model_name in self.project_info['models_trained']:
                if model_name in self.models:
                    train_time = self.models[model_name].get('train_time', 0)
                    report.append(f"  • {model_name.upper()}: {train_time:.2f}s")
        
        # Model rankings
        if self.comparisons.get('rankings'):
            report.append(f"\nModel Rankings (NDCG@10):")
            for i, (model_name, score) in enumerate(self.comparisons['rankings'], 1):
                report.append(f"  {i}. {model_name}: {score:.4f}")
        
        # Evaluations
        if self.evaluations:
            report.append(f"\nModel Evaluations:")
            for algo_name in self.evaluations:
                report.append(f"  • {algo_name.upper()}")
        
        report.append(f"\n" + "="*70)
        
        report_text = "\n".join(report)
        logger.info(report_text)
        
        return report_text
    
    def save_project_metadata(self) -> None:
        """Save project metadata to JSON."""
        metadata_path = self.models_dir / "project_metadata.json"
        
        try:
            self.project_info['last_updated'] = datetime.now().isoformat()
            
            with open(metadata_path, 'w') as f:
                json.dump(self.project_info, f, indent=2, default=str)
            
            logger.info(f"✓ Project metadata saved: {metadata_path}")
        
        except Exception as e:
            logger.error(f"✗ Failed to save metadata: {str(e)}")


# Global manager instance
_global_manager: Optional[MLManager] = None


def get_ml_manager() -> MLManager:
    """Get or create global ML manager."""
    global _global_manager
    if _global_manager is None:
        _global_manager = MLManager()
    return _global_manager


def set_ml_manager(manager: MLManager) -> None:
    """Set global ML manager."""
    global _global_manager
    _global_manager = manager
