"""
MovieReco ML Pipeline - Complete Machine Learning System

This package implements a production-grade ML recommendation system with:
- Multiple algorithms (Collaborative Filtering, Content-Based, Matrix Factorization)
- Advanced evaluation metrics
- Hyperparameter tuning
- A/B testing framework
- Cold start solutions
- Model comparison and blending

Structure:
├── collaborative_filtering.py  → User-user/Item-item CF
├── content_based.py           → Content-based recommendations (TF-IDF)
├── matrix_factorization.py    → SVD-based recommendations
├── feature_engineering.py     → Feature extraction & normalization
├── data_loader.py             → CSV loading & validation
├── csv_generator.py           → Synthetic data generation
├── model_evaluator.py         → Comprehensive evaluation metrics
├── model_comparison.py        → Algorithm comparison framework
├── hyperparameter_tuning.py   → Grid search & optimization
├── recommendation_blending.py → Multi-model ensemble
├── cold_start_handler.py      → New user/item solutions
├── performance_cache.py       → Inference caching & TTL
└── ab_testing.py              → A/B testing framework

Core Algorithms:
- UserUserCollaborativeFiltering: User-user CF with cosine similarity
- ContentBasedRecommender: TF-IDF genre-based recommendations
- MatrixFactorization: SVD-based latent factor model

Usage Examples:
    from app.ml import UserUserCollaborativeFiltering, DataLoader, ModelEvaluator
    from app.ml import ContentBasedRecommender, MatrixFactorization
    from app.ml import RecommendationBlender, ModelComparison
    
    # Train model
    loader = DataLoader()
    ratings_df = loader.load_ratings()
    model = UserUserCollaborativeFiltering(k_neighbors=10)
    model.train(ratings_df)
    
    # Get recommendations
    recs = await model.recommend('user_1', limit=10)
    
    # Compare models
    comparison = ModelComparison()
    comparison.register_model('cf', model)
    results = await comparison.compare_on_test_set(test_users)
    
    # Blend recommendations
    blender = RecommendationBlender()
    blender.add_model('cf', model, weight=0.6)
    blended = await blender.blend_recommendations('user_1')
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
from .csv_generator import CSVDataGenerator
from .feature_engineering import FeatureEngineer

# Evaluation & comparison
from .model_evaluator import ModelEvaluator
from .model_comparison import ModelComparison

# Advanced features
from .recommendation_blending import RecommendationBlender
from .cold_start_handler import ColdStartHandler
from .hyperparameter_tuning import HyperparameterTuner
from .performance_cache import PerformanceCache, get_global_cache, set_global_cache
from .ab_testing import ABTest, ABTestManager

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
    "CSVDataGenerator",
    "FeatureEngineer",
    
    # Evaluation
    "ModelEvaluator",
    "ModelComparison",
    
    # Advanced
    "RecommendationBlender",
    "ColdStartHandler",
    "HyperparameterTuner",
    "PerformanceCache",
    "get_global_cache",
    "set_global_cache",
    "ABTest",
    "ABTestManager",
]

__version__ = "2.0.0"  # Bumped for complete ML system
__author__ = "MovieReco Team"
__description__ = "Production-grade ML recommendation system"
