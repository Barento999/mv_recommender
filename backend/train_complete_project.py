"""
Complete ML Project Training Script

THIS SCRIPT IS FOR REFERENCE ONLY.
The actual ML pipeline is now AUTO-INITIALIZED on app startup!

See: backend/app/ml/pipeline.py for production ML initialization.

The ML pipeline automatically executes on application startup:
1. Data is loaded from CSV
2. Models are trained (CF, Content-Based)
3. Performance caching is initialized
4. All models are ready for inference

Usage:
    # Option 1: Use automatic pipeline (RECOMMENDED)
    cd backend
    ./venv/bin/python -m uvicorn app.main:app --reload
    # ML pipeline initializes automatically on startup

    # Option 2: Run this training script (optional)
    python train_complete_project.py

The automatic initialization is integrated into app/main.py lifespan hooks.
"""

import asyncio
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


async def run_complete_ml_project():
    """Run the complete ML project pipeline."""
    
    try:
        from app.ml.ml_manager import MLManager
        
        # Initialize ML Manager
        logger.info("\n" + "="*70)
        logger.info("🚀 COMPLETE ML PROJECT PIPELINE")
        logger.info("="*70)
        
        manager = MLManager(data_dir="data", models_dir="models")
        
        # =====================================================================
        # Step 1: Prepare Data
        # =====================================================================
        success = await manager.prepare_data(validate=True)
        if not success:
            logger.error("✗ Data preparation failed")
            return 1
        
        # =====================================================================
        # Step 2: Train Models
        # =====================================================================
        train_results = await manager.train_models(
            algorithms=['cf', 'content', 'mf']
        )
        
        if not train_results:
            logger.error("✗ Model training failed")
            return 1
        
        # =====================================================================
        # Step 3: Evaluate Models
        # =====================================================================
        eval_results = await manager.evaluate_models()
        
        if not eval_results:
            logger.warning("⚠ Model evaluation failed")
        
        # =====================================================================
        # Step 4: Compare Models
        # =====================================================================
        comp_results = await manager.compare_models()
        
        if not comp_results:
            logger.warning("⚠ Model comparison failed")
        
        # =====================================================================
        # Step 5: Hyperparameter Tuning
        # =====================================================================
        logger.info("\n" + "="*70)
        logger.info("[MLManager] STEP 5: HYPERPARAMETER TUNING")
        logger.info("="*70)
        
        logger.info("\nTuning Collaborative Filtering model...")
        cf_tuning = await manager.tune_hyperparameters('cf')
        
        if cf_tuning:
            logger.info(f"✓ CF Tuning complete")
            logger.info(f"  Best params: {cf_tuning.get('best_params')}")
            logger.info(f"  Best score: {cf_tuning.get('best_score'):.4f}")
        
        logger.info("\nTuning Matrix Factorization model...")
        mf_tuning = await manager.tune_hyperparameters('mf')
        
        if mf_tuning:
            logger.info(f"✓ MF Tuning complete")
            logger.info(f"  Best params: {mf_tuning.get('best_params')}")
            logger.info(f"  Best score: {mf_tuning.get('best_score'):.4f}")
        
        # =====================================================================
        # Step 6: Save Models
        # =====================================================================
        logger.info("\n" + "="*70)
        logger.info("[MLManager] STEP 6: MODEL PERSISTENCE")
        logger.info("="*70)
        
        save_results = manager.save_models()
        logger.info(f"✓ Saved {len(save_results)} models")
        
        # =====================================================================
        # Step 7: Generate Report
        # =====================================================================
        report = manager.generate_project_report()
        
        # Save metadata
        manager.save_project_metadata()
        
        # =====================================================================
        # Final Summary
        # =====================================================================
        logger.info("\n" + "="*70)
        logger.info("✅ ML PROJECT PIPELINE COMPLETE")
        logger.info("="*70)
        
        logger.info(f"\nResults Summary:")
        logger.info(f"  ✓ Data: {len(manager.movies_df)} movies, {len(manager.users_df)} users")
        logger.info(f"  ✓ Models trained: {len(train_results)}")
        logger.info(f"  ✓ Models evaluated: {len(eval_results)}")
        logger.info(f"  ✓ Models compared: {len(comp_results.get('rankings', []))}")
        logger.info(f"  ✓ Models saved: {len(save_results)}")
        
        logger.info(f"\nBest Model (by NDCG@10):")
        if comp_results.get('rankings'):
            best_model, best_score = comp_results['rankings'][0]
            logger.info(f"  {best_model}: {best_score:.4f}")
        
        logger.info(f"\nOutput Files:")
        logger.info(f"  • Models: models/")
        logger.info(f"  • Metadata: models/project_metadata.json")
        
        logger.info(f"\n" + "="*70)
        logger.info("🎉 Ready for deployment!")
        logger.info("="*70 + "\n")
        
        return 0
    
    except Exception as e:
        logger.error(f"✗ Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_complete_ml_project())
    sys.exit(exit_code)
