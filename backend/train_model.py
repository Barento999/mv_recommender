"""
ML Model Training Pipeline

Production script for training recommendation models from CSV data.
Handles data loading, model training, evaluation, and persistence.

Usage:
    python train_model.py                          # Use defaults (2000 movies, 150 users)
    python train_model.py --movies 5000 --users 500  # Custom sizes
    python train_model.py --movies data/movies.csv --users data/users.csv --ratings data/ratings.csv
"""

import argparse
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(name)s] %(message)s'
)
logger = logging.getLogger('MLTrainer')


def main():
    parser = argparse.ArgumentParser(description='Train ML recommendation model')
    parser.add_argument('--movies', type=str, default='data/movies.csv',
                        help='Path to movies CSV or number of movies to generate')
    parser.add_argument('--users', type=str, default='data/users.csv',
                        help='Path to users CSV or number of users to generate')
    parser.add_argument('--ratings', type=str, default='data/ratings.csv',
                        help='Path to ratings CSV')
    parser.add_argument('--output', type=str, default='models',
                        help='Output directory for trained model')
    parser.add_argument('--k-neighbors', type=int, default=10,
                        help='Number of neighbors for CF')
    parser.add_argument('--generate', action='store_true',
                        help='Generate CSV data before training')
    parser.add_argument('--data-dir', type=str, default='data',
                        help='Directory for generated CSVs')
    
    args = parser.parse_args()
    
    logger.info("="*70)
    logger.info("ML RECOMMENDATION MODEL TRAINING PIPELINE")
    logger.info("="*70)
    
    try:
        # Import ML modules
        from app.ml.data_loader import DataLoader
        from app.ml.collaborative_filtering import UserUserCollaborativeFiltering, set_global_model
        from pathlib import Path
        
        # Step 1: Load data from CSV files
        logger.info("\n[STEP 1] Loading data from CSV files...")
        
        # Use pre-generated CSV files in backend/data/
        movies_path = "data/movies.csv"
        users_path = "data/users.csv"
        ratings_path = "data/ratings.csv"
        
        if not Path(movies_path).exists() or not Path(ratings_path).exists():
            logger.error(f"CSV files not found in data/ directory")
            logger.error(f"Expected: {movies_path}, {users_path}, {ratings_path}")
            return 1
            users_path = args.users
            ratings_path = args.ratings
            logger.info(f"Using provided CSV files:")
            logger.info(f"  Movies: {movies_path}")
            logger.info(f"  Users: {users_path}")
            logger.info(f"  Ratings: {ratings_path}")
        
        # Step 2: Load and validate data
        logger.info("\n[STEP 2] Loading and validating data...")
        
        loader = DataLoader()
        movies_df = loader.load_movies(movies_path)
        users_df = loader.load_users(users_path)
        ratings_df = loader.load_ratings(ratings_path)
        
        summary = loader.get_data_summary()
        logger.info(f"Data summary: {summary}")
        
        # Step 3: Train model
        logger.info("\n[STEP 3] Training model...")
        
        model = create_model_from_csv(
            ratings_csv=ratings_path,
            movies_csv=movies_path,
            users_csv=users_path,
            k_neighbors=args.k_neighbors
        )
        
        if not model or not model.is_trained:
            logger.error("✗ Model training failed!")
            return 1
        
        # Step 4: Model evaluation
        logger.info("\n[STEP 4] Model evaluation...")
        
        metrics = model.get_metrics()
        logger.info(f"Model metrics:")
        for key, value in metrics.items():
            if isinstance(value, float):
                logger.info(f"  {key}: {value:.4f}" if value < 100 else f"  {key}: {int(value)}")
            else:
                logger.info(f"  {key}: {value}")
        
        # Step 5: Save model
        logger.info("\n[STEP 5] Persisting model...")
        
        output_dir = Path(args.output)
        output_dir.mkdir(exist_ok=True)
        model_path = output_dir / "collaborative_filtering_model.pkl"
        
        if model.save(str(model_path)):
            logger.info(f"✓ Model saved to: {model_path}")
        else:
            logger.warning("Could not save model to disk")
        
        # Step 6: Set as global model
        logger.info("\n[STEP 6] Activating model...")
        set_global_model(model)
        logger.info("✓ Model set as global instance (ready for API)")
        
        logger.info("\n" + "="*70)
        logger.info("✓ TRAINING COMPLETE!")
        logger.info("="*70)
        logger.info(f"\nModel ready for production:")
        logger.info(f"  - Users: {metrics.get('n_users', 'N/A')}")
        logger.info(f"  - Movies: {metrics.get('n_movies', 'N/A')}")
        logger.info(f"  - Ratings: {metrics.get('n_ratings', 'N/A')}")
        logger.info(f"  - Training time: {metrics.get('training_time_seconds', 'N/A'):.3f}s")
        logger.info(f"\nNext: Start the API to serve recommendations!")
        
        return 0
        
    except Exception as e:
        logger.error(f"✗ Training pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
