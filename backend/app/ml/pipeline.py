"""
ML Pipeline - Complete Recommendation System Pipeline

Handles the complete ML pipeline:
1. Load data from CSV
2. Train models
3. Cache models globally
4. Provide inference API

This module runs on application startup and provides
global model access for recommendations.
"""

import logging
import time
from pathlib import Path
from typing import Optional, Dict, Tuple
import pandas as pd

logger = logging.getLogger(__name__)

# Global model instances
_global_model = None
_global_cf_model = None
_global_content_model = None
_global_cache = None


def get_model():
    """Get trained recommendation model."""
    return _global_model


def get_cf_model():
    """Get trained collaborative filtering model."""
    return _global_cf_model


def get_content_model():
    """Get trained content-based model."""
    return _global_content_model


def get_cache():
    """Get global cache instance."""
    return _global_cache


async def initialize_ml_pipeline() -> bool:
    """
    Initialize and train the complete ML pipeline.
    
    Called on application startup.
    Loads data, trains models, and sets up caching.
    
    Returns:
        True if successful, False otherwise
    """
    global _global_model, _global_cf_model, _global_content_model, _global_cache
    
    try:
        logger.info("="*70)
        logger.info("ML PIPELINE INITIALIZATION")
        logger.info("="*70)
        
        # =====================================================================
        # Step 1: Load Data
        # =====================================================================
        logger.info("\n[1/4] Loading CSV Data...")
        start_time = time.time()
        
        from app.ml.data_loader import DataLoader
        
        loader = DataLoader("data")
        movies_df = loader.load_movies("data/movies.csv")
        users_df = loader.load_users("data/users.csv")
        ratings_df = loader.load_ratings("data/ratings.csv")
        
        load_time = time.time() - start_time
        logger.info(f"✓ Data loaded in {load_time:.2f}s")
        logger.info(f"  Movies: {len(movies_df)}")
        logger.info(f"  Users: {len(users_df)}")
        logger.info(f"  Ratings: {len(ratings_df)}")
        
        # =====================================================================
        # Step 2: Train Collaborative Filtering Model
        # =====================================================================
        logger.info("\n[2/4] Training Collaborative Filtering Model...")
        start_time = time.time()
        
        from app.ml.collaborative_filtering import UserUserCollaborativeFiltering
        
        cf_model = UserUserCollaborativeFiltering(k_neighbors=10, model_name="production_cf_v1")
        cf_success = cf_model.train(ratings_df, movies_df, users_df)
        
        if not cf_success:
            logger.error("✗ CF model training failed")
            return False
        
        train_time = time.time() - start_time
        logger.info(f"✓ CF Model trained in {train_time:.2f}s")
        
        metrics = cf_model.get_metrics()
        logger.info(f"  Algorithm: {metrics.get('algorithm', 'Unknown')}")
        logger.info(f"  K-neighbors: {cf_model.k_neighbors}")
        logger.info(f"  Training time: {metrics.get('training_time_seconds', 0):.3f}s")
        
        _global_cf_model = cf_model
        _global_model = cf_model  # Set as default model
        
        # =====================================================================
        # Step 3: Train Content-Based Model
        # =====================================================================
        logger.info("\n[3/4] Training Content-Based Model...")
        start_time = time.time()
        
        from app.ml.content_based import ContentBasedRecommender
        
        cb_model = ContentBasedRecommender(model_name="production_content_v1")
        cb_success = cb_model.train(movies_df, ratings_df)
        
        if not cb_success:
            logger.warning("⚠ Content-based model training failed (non-critical)")
            _global_content_model = None
        else:
            train_time = time.time() - start_time
            logger.info(f"✓ Content-Based Model trained in {train_time:.2f}s")
            _global_content_model = cb_model
        
        # =====================================================================
        # Step 4: Initialize Performance Cache
        # =====================================================================
        logger.info("\n[4/4] Initializing Performance Cache...")
        
        from app.ml.performance_cache import PerformanceCache
        
        cache = PerformanceCache(ttl_seconds=3600, max_entries=10000)
        _global_cache = cache
        
        logger.info(f"✓ Cache initialized")
        logger.info(f"  TTL: 3600 seconds")
        logger.info(f"  Max entries: 10000")
        
        # =====================================================================
        # Pipeline Complete
        # =====================================================================
        logger.info("\n" + "="*70)
        logger.info("✓ ML PIPELINE INITIALIZED SUCCESSFULLY")
        logger.info("="*70)
        logger.info(f"\nModels Ready:")
        logger.info(f"  • Collaborative Filtering: {'✓' if _global_cf_model else '✗'}")
        logger.info(f"  • Content-Based: {'✓' if _global_content_model else '✗'}")
        logger.info(f"  • Cache: ✓")
        logger.info(f"\nThe system is ready for recommendations!")
        logger.info("="*70 + "\n")
        
        return True
    
    except Exception as e:
        logger.error(f"✗ ML Pipeline initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def get_recommendation(user_id: str, limit: int = 10, 
                            model_type: str = "cf") -> list:
    """
    Get recommendations for a user using trained model.
    
    Args:
        user_id: User ID
        limit: Number of recommendations
        model_type: 'cf' for collaborative filtering, 'content' for content-based
        
    Returns:
        List of (movie_id, score) tuples
    """
    try:
        # Check cache first
        if _global_cache:
            cache_key = _global_cache.get_cache_key(user_id, model_type, limit)
            cached = _global_cache.get(cache_key)
            if cached:
                logger.debug(f"Cache hit for {user_id}")
                return cached
        
        # Get model
        if model_type == "content" and _global_content_model:
            model = _global_content_model
        else:
            model = _global_cf_model
        
        if not model:
            logger.warning(f"Model type '{model_type}' not available")
            return []
        
        # Get recommendations
        recommendations = await model.recommend(user_id, limit=limit)
        
        # Cache results
        if _global_cache and recommendations:
            cache_key = _global_cache.get_cache_key(user_id, model_type, limit)
            _global_cache.set(cache_key, recommendations)
        
        return recommendations
    
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return []


async def get_similar_movies(movie_id: str, limit: int = 10) -> list:
    """
    Get movies similar to a given movie.
    
    Args:
        movie_id: Movie ID
        limit: Number of similar movies
        
    Returns:
        List of (movie_id, similarity) tuples
    """
    try:
        if not _global_content_model:
            logger.warning("Content-based model not available")
            return []
        
        similar = _global_content_model.get_similar_movies(movie_id, limit=limit)
        return similar
    
    except Exception as e:
        logger.error(f"Error getting similar movies: {str(e)}")
        return []


def get_pipeline_status() -> Dict:
    """
    Get status of ML pipeline.
    
    Returns:
        Dict with pipeline status
    """
    return {
        'cf_model': _global_cf_model is not None,
        'content_model': _global_content_model is not None,
        'cache': _global_cache is not None,
        'cache_stats': _global_cache.get_stats() if _global_cache else None,
    }
