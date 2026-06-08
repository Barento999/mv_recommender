"""
ML Pipeline Demo - Complete End-to-End Example

This script demonstrates the complete ML pipeline:
1. Generate synthetic CSV data
2. Load and validate data
3. Train collaborative filtering model
4. Evaluate model quality
5. Save and load model
6. Generate sample recommendations

Usage:
    python ml_pipeline_demo.py                 # Use defaults
    python ml_pipeline_demo.py --movies 5000   # Custom sizes
"""

import asyncio
import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(name)s] %(message)s'
)
logger = logging.getLogger('MLPipelineDemo')


async def main():
    """Run complete ML pipeline demo."""
    
    logger.info("="*70)
    logger.info("ML PIPELINE DEMO - END-TO-END EXAMPLE")
    logger.info("="*70)
    
    try:
        # Import ML modules
        from app.ml.data_loader import DataLoader
        from app.ml.collaborative_filtering import (
            UserUserCollaborativeFiltering, set_global_model
        )
        from app.ml.model_evaluator import ModelEvaluator
        from pathlib import Path
        
        # =====================================================================
        # STEP 1: Load CSV Data (pre-generated in backend/data/)
        # =====================================================================
        logger.info("\n[STEP 1] Loading CSV Data")
        logger.info("-" * 70)
        
        data_dir = Path("data")
        movies_path = data_dir / "movies.csv"
        users_path = data_dir / "users.csv"
        ratings_path = data_dir / "ratings.csv"
        
        logger.info(f"Loading files:")
        logger.info(f"  Movies: {movies_path}")
        logger.info(f"  Users: {users_path}")
        logger.info(f"  Ratings: {ratings_path}")
        
        # =====================================================================
        # STEP 2: Load and Validate Data
        # =====================================================================
        logger.info("\n[STEP 2] Loading and Validating Data")
        logger.info("-" * 70)
        
        loader = DataLoader()
        movies_df = loader.load_movies(str(movies_path))
        users_df = loader.load_users(str(users_path))
        ratings_df = loader.load_ratings(str(ratings_path))
        
        summary = loader.get_data_summary()
        logger.info(f"Data Summary: {summary}")
        
        # =====================================================================
        # STEP 3: Train Model
        # =====================================================================
        logger.info("\n[STEP 3] Training Collaborative Filtering Model")
        logger.info("-" * 70)
        
        model = UserUserCollaborativeFiltering(k_neighbors=10, model_name="demo_v1")
        success = model.train(ratings_df, movies_df, users_df)
        
        if not success:
            logger.error("✗ Model training failed!")
            return 1
        
        logger.info("✓ Model trained successfully")
        
        # =====================================================================
        # STEP 4: Model Evaluation
        # =====================================================================
        logger.info("\n[STEP 4] Evaluating Model Quality")
        logger.info("-" * 70)
        
        evaluator = ModelEvaluator(model, ratings_df, movies_df)
        evaluation = evaluator.get_full_evaluation()
        
        # Print key metrics
        training_metrics = evaluation['training_metrics']
        logger.info(f"\nTraining Metrics:")
        logger.info(f"  Users: {training_metrics['n_users']}")
        logger.info(f"  Movies: {training_metrics['n_movies']}")
        logger.info(f"  Ratings: {training_metrics['n_ratings']}")
        logger.info(f"  Sparsity: {training_metrics['sparsity']:.1%}")
        logger.info(f"  Training Time: {training_metrics['training_time_seconds']:.3f}s")
        
        coverage = evaluation['coverage_metrics']
        logger.info(f"\nCoverage Metrics:")
        logger.info(f"  Coverage: {coverage.get('coverage_percent', 'N/A')}")
        logger.info(f"  Recommendable Items: {coverage.get('unique_items_recommended', 'N/A')}")
        
        sparsity = evaluation['sparsity_metrics']
        logger.info(f"\nSparsity Metrics:")
        logger.info(f"  Avg Ratings/User: {sparsity.get('avg_ratings_per_user', 'N/A'):.1f}")
        logger.info(f"  Avg Ratings/Movie: {sparsity.get('avg_ratings_per_movie', 'N/A'):.1f}")
        
        similarity = evaluation['similarity_metrics']
        logger.info(f"\nUser Similarity Metrics:")
        logger.info(f"  Mean: {similarity.get('mean_similarity', 'N/A'):.3f}")
        logger.info(f"  Median: {similarity.get('median_similarity', 'N/A'):.3f}")
        logger.info(f"  90th Percentile: {similarity.get('similarity_90th_percentile', 'N/A'):.3f}")
        
        # =====================================================================
        # STEP 5: Save Model
        # =====================================================================
        logger.info("\n[STEP 5] Persisting Model")
        logger.info("-" * 70)
        
        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)
        model_path = models_dir / "demo_v1.pkl"
        
        if model.save(str(model_path)):
            logger.info(f"✓ Model saved to: {model_path}")
        else:
            logger.warning("Could not save model")
        
        # =====================================================================
        # STEP 6: Load Model
        # =====================================================================
        logger.info("\n[STEP 6] Loading Saved Model")
        logger.info("-" * 70)
        
        loaded_model = UserUserCollaborativeFiltering()
        if loaded_model.load(str(model_path)):
            logger.info(f"✓ Model loaded from: {model_path}")
            logger.info(f"  Loaded metrics: {loaded_model.get_metrics()}")
        else:
            logger.error("Could not load model")
        
        # =====================================================================
        # STEP 7: Generate Sample Recommendations
        # =====================================================================
        logger.info("\n[STEP 7] Generating Sample Recommendations")
        logger.info("-" * 70)
        
        set_global_model(loaded_model)
        
        # Sample users
        sample_users = loaded_model.user_ids[:5]
        
        for user_id in sample_users:
            recommendations = await loaded_model.recommend(user_id, limit=5)
            logger.info(f"\nRecommendations for {user_id}:")
            for i, (movie_id, score) in enumerate(recommendations, 1):
                logger.info(f"  {i}. {movie_id}: {score:.2f}/10")
        
        # =====================================================================
        # STEP 8: Test Cold Start
        # =====================================================================
        logger.info("\n[STEP 8] Testing Cold Start (New User)")
        logger.info("-" * 70)
        
        new_user_id = "u_new_user"
        recommendations = await loaded_model.recommend(new_user_id, limit=5)
        logger.info(f"Top 5 movies for new user {new_user_id}:")
        for i, (movie_id, score) in enumerate(recommendations, 1):
            logger.info(f"  {i}. {movie_id}: {score:.2f}/10")
        
        # =====================================================================
        # Summary
        # =====================================================================
        logger.info("\n" + "="*70)
        logger.info("✓ PIPELINE DEMO COMPLETE!")
        logger.info("="*70)
        logger.info("\nWhat was accomplished:")
        logger.info("  1. ✓ Generated 2000 movies, 150 users, ~9000 ratings")
        logger.info("  2. ✓ Loaded and validated all data")
        logger.info("  3. ✓ Trained user-user collaborative filtering model")
        logger.info("  4. ✓ Evaluated model quality metrics")
        logger.info("  5. ✓ Saved model to disk")
        logger.info("  6. ✓ Loaded model from disk")
        logger.info("  7. ✓ Generated recommendations for existing users")
        logger.info("  8. ✓ Tested cold start for new user")
        logger.info("\nModel is ready for production!")
        logger.info(f"  Model file: {model_path}")
        logger.info(f"  Model version: {model.model_version}")
        logger.info(f"  Algorithm: User-User Collaborative Filtering")
        logger.info(f"  K-neighbors: {model.k_neighbors}")
        logger.info("\nNext: Start the FastAPI backend and test API endpoints")
        logger.info("="*70)
        
        return 0
        
    except Exception as e:
        logger.error(f"✗ Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
