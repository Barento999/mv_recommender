"""
MovieReco ML Pipeline - Complete Machine Learning System

Streamlined production-grade ML recommendation system with:
- 3 core algorithms (Collaborative Filtering, Content-Based, Matrix Factorization)
- Complete ML project management (training, evaluation, comparison, tuning)
- Production integration (app startup initialization)
- Performance caching & monitoring

Structure:
├── collaborative_filtering.py  → User-user CF (main algorithm)
├── content_based.py           → Content-based recommendations
├── matrix_factorization.py    → SVD-based recommendations
├── data_loader.py             → CSV loading & validation
├── ml_manager.py              → Complete ML orchestration
├── pipeline.py                → Production integration
├── performance_cache.py       → Inference caching
├── recommendation_blending.py → Model ensembling
└── __init__.py                → Package exports

Core Usage:
    # Training & Evaluation
    from app.ml import MLManager
    manager = MLManager()
    await manager.prepare_data()
    await manager.train_models(['cf', 'content', 'mf'])
    await manager.evaluate_models()
    
    # Production recommendations
    from app.ml.pipeline import get_recommendation
    recs = await get_recommendation('user_1', limit=10)
"""

# Core models
from .collaborative_filtering import (
    UserUserCollaborativeFiltering,
    set_global_model,
    get_global_model
)
from .content_based import ContentBasedRecommender
from .matrix_factorization import MatrixFactorization

# Data handling
from .data_loader import DataLoader

# ML management
from .ml_manager import MLManager

# Advanced features
from .recommendation_blending import RecommendationBlender
from .performance_cache import PerformanceCache, get_global_cache, set_global_cache

__all__ = [
    # Core models
    "UserUserCollaborativeFiltering",
    "ContentBasedRecommender",
    "MatrixFactorization",
    
    # Model management
    "set_global_model",
    "get_global_model",
    
    # Data handling
    "DataLoader",
    
    # ML management
    "MLManager",
    
    # Advanced
    "RecommendationBlender",
    "PerformanceCache",
    "get_global_cache",
    "set_global_cache",
]

__version__ = "2.0.0"  # Streamlined complete system
__author__ = "MovieReco Team"
__description__ = "Production-grade ML recommendation system"
