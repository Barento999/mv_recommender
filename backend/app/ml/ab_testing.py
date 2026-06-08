"""
A/B Testing Framework

Runs A/B tests to compare recommendation algorithms in production.
Tracks metrics and provides statistical analysis.
"""

import hashlib
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from enum import Enum
import logging
import numpy as np

logger = logging.getLogger(__name__)


class TestVariant(Enum):
    """Test variant (Control or Treatment)."""
    CONTROL = "control"
    TREATMENT = "treatment"


class ABTest:
    """A/B test configuration and tracking."""
    
    def __init__(self, test_id: str, test_name: str, description: str = "",
                 control_model: str = "user_user_cf", treatment_model: str = "matrix_factorization",
                 split_ratio: float = 0.5, duration_days: int = 7):
        """
        Initialize A/B test.
        
        Args:
            test_id: Unique test identifier
            test_name: Human-readable test name
            description: Test description
            control_model: Model name for control group
            treatment_model: Model name for treatment group
            split_ratio: Fraction of users in treatment group (0.5 = 50/50 split)
            duration_days: Test duration in days
        """
        self.test_id = test_id
        self.test_name = test_name
        self.description = description
        self.control_model = control_model
        self.treatment_model = treatment_model
        self.split_ratio = split_ratio
        self.duration_days = duration_days
        
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(days=duration_days)
        self.is_active = True
        
        # Results tracking
        self.results = {
            'control': {
                'n_impressions': 0,
                'n_clicks': 0,
                'n_conversions': 0,
                'ratings_given': [],
                'avg_rating': 0.0,
                'users': set(),
            },
            'treatment': {
                'n_impressions': 0,
                'n_clicks': 0,
                'n_conversions': 0,
                'ratings_given': [],
                'avg_rating': 0.0,
                'users': set(),
            }
        }
        
        logger.info(f"[ABTest] Created: {test_name} ({test_id})")
        logger.info(f"[ABTest] Control: {control_model}, Treatment: {treatment_model}")
        logger.info(f"[ABTest] Split: {split_ratio*100:.0f}% treatment, {(1-split_ratio)*100:.0f}% control")
    
    def assign_variant(self, user_id: str) -> TestVariant:
        """
        Assign user to variant based on hash.
        Deterministic: same user always gets same variant.
        
        Args:
            user_id: User identifier
            
        Returns:
            TestVariant (CONTROL or TREATMENT)
        """
        # Hash user_id to consistent variant
        hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        
        if (hash_value % 100) < (self.split_ratio * 100):
            return TestVariant.TREATMENT
        else:
            return TestVariant.CONTROL
    
    def record_impression(self, user_id: str, recommendations: List[Tuple[str, float]]) -> None:
        """
        Record when recommendations are shown to user.
        
        Args:
            user_id: User ID
            recommendations: List of recommendations shown
        """
        variant = self.assign_variant(user_id)
        variant_key = variant.value
        
        self.results[variant_key]['n_impressions'] += 1
        self.results[variant_key]['users'].add(user_id)
        
        logger.debug(f"[ABTest] Impression: {user_id} -> {variant_key} ({len(recommendations)} items)")
    
    def record_click(self, user_id: str, movie_id: str) -> None:
        """
        Record when user clicks on a recommendation.
        
        Args:
            user_id: User ID
            movie_id: Movie ID clicked
        """
        variant = self.assign_variant(user_id)
        variant_key = variant.value
        
        self.results[variant_key]['n_clicks'] += 1
        
        logger.debug(f"[ABTest] Click: {user_id} ({variant_key}) -> {movie_id}")
    
    def record_rating(self, user_id: str, movie_id: str, rating: float) -> None:
        """
        Record when user rates a movie (conversion).
        
        Args:
            user_id: User ID
            movie_id: Movie ID rated
            rating: Rating value
        """
        variant = self.assign_variant(user_id)
        variant_key = variant.value
        
        self.results[variant_key]['n_conversions'] += 1
        self.results[variant_key]['ratings_given'].append(rating)
        
        # Update average
        ratings = self.results[variant_key]['ratings_given']
        self.results[variant_key]['avg_rating'] = np.mean(ratings)
        
        logger.debug(f"[ABTest] Rating: {user_id} ({variant_key}) -> {movie_id}: {rating}")
    
    def get_metrics(self) -> Dict:
        """
        Calculate test metrics.
        
        Returns:
            Dict with metrics for both variants
        """
        metrics = {}
        
        for variant_key in ['control', 'treatment']:
            result = self.results[variant_key]
            
            ctr = (result['n_clicks'] / result['n_impressions'] * 100) if result['n_impressions'] > 0 else 0
            conversion_rate = (result['n_conversions'] / result['n_clicks'] * 100) if result['n_clicks'] > 0 else 0
            
            metrics[variant_key] = {
                'n_users': len(result['users']),
                'n_impressions': result['n_impressions'],
                'n_clicks': result['n_clicks'],
                'n_conversions': result['n_conversions'],
                'ctr': ctr,
                'conversion_rate': conversion_rate,
                'avg_rating': float(result['avg_rating']),
                'model': self.control_model if variant_key == 'control' else self.treatment_model,
            }
        
        return metrics
    
    def get_statistical_significance(self) -> Dict:
        """
        Calculate statistical significance of differences.
        Uses chi-square test for conversion rates.
        
        Returns:
            Dict with p-values and significance
        """
        try:
            from scipy.stats import chi2_contingency
            
            # Build contingency table
            control_conversions = self.results['control']['n_conversions']
            control_non_conversions = self.results['control']['n_clicks'] - control_conversions
            treatment_conversions = self.results['treatment']['n_conversions']
            treatment_non_conversions = self.results['treatment']['n_clicks'] - treatment_conversions
            
            contingency_table = [
                [control_conversions, control_non_conversions],
                [treatment_conversions, treatment_non_conversions]
            ]
            
            chi2, p_value, dof, expected = chi2_contingency(contingency_table)
            
            is_significant = p_value < 0.05  # 95% confidence
            
            return {
                'chi2': float(chi2),
                'p_value': float(p_value),
                'dof': dof,
                'is_significant': is_significant,
                'confidence_level': 95 if is_significant else 0,
            }
        
        except Exception as e:
            logger.warning(f"[ABTest] Could not calculate significance: {str(e)}")
            return {}
    
    def get_report(self) -> str:
        """Generate A/B test report."""
        metrics = self.get_metrics()
        stats = self.get_statistical_significance()
        
        duration_elapsed = (datetime.now() - self.start_time).days
        remaining_days = (self.end_time - datetime.now()).days
        
        report = []
        report.append("="*70)
        report.append("A/B TEST REPORT")
        report.append("="*70)
        report.append("")
        report.append(f"Test: {self.test_name} ({self.test_id})")
        report.append(f"Description: {self.description}")
        report.append("")
        report.append(f"Duration: {self.duration_days} days ({duration_elapsed} elapsed, {remaining_days} remaining)")
        report.append(f"Status: {'Active' if self.is_active else 'Completed'}")
        report.append("")
        
        # Control group
        report.append("CONTROL GROUP")
        report.append(f"Model: {metrics['control']['model']}")
        report.append(f"Users: {metrics['control']['n_users']}")
        report.append(f"Impressions: {metrics['control']['n_impressions']}")
        report.append(f"Clicks: {metrics['control']['n_clicks']}")
        report.append(f"Conversions: {metrics['control']['n_conversions']}")
        report.append(f"CTR: {metrics['control']['ctr']:.2f}%")
        report.append(f"Conversion Rate: {metrics['control']['conversion_rate']:.2f}%")
        report.append(f"Avg Rating: {metrics['control']['avg_rating']:.2f}")
        report.append("")
        
        # Treatment group
        report.append("TREATMENT GROUP")
        report.append(f"Model: {metrics['treatment']['model']}")
        report.append(f"Users: {metrics['treatment']['n_users']}")
        report.append(f"Impressions: {metrics['treatment']['n_impressions']}")
        report.append(f"Clicks: {metrics['treatment']['n_clicks']}")
        report.append(f"Conversions: {metrics['treatment']['n_conversions']}")
        report.append(f"CTR: {metrics['treatment']['ctr']:.2f}%")
        report.append(f"Conversion Rate: {metrics['treatment']['conversion_rate']:.2f}%")
        report.append(f"Avg Rating: {metrics['treatment']['avg_rating']:.2f}")
        report.append("")
        
        # Statistical significance
        if stats:
            report.append("STATISTICAL SIGNIFICANCE")
            report.append(f"Chi-Square: {stats.get('chi2', 'N/A')}")
            report.append(f"P-Value: {stats.get('p_value', 'N/A')}")
            report.append(f"Significant (p<0.05): {stats.get('is_significant', False)}")
        
        report.append("="*70)
        
        return "\n".join(report)


class ABTestManager:
    """Manage multiple A/B tests."""
    
    def __init__(self):
        """Initialize test manager."""
        self.tests: Dict[str, ABTest] = {}
        logger.info("[ABTestManager] Initialized")
    
    def create_test(self, test_id: str, test_name: str, **kwargs) -> ABTest:
        """Create new A/B test."""
        test = ABTest(test_id, test_name, **kwargs)
        self.tests[test_id] = test
        return test
    
    def get_test(self, test_id: str) -> Optional[ABTest]:
        """Get test by ID."""
        return self.tests.get(test_id)
    
    def get_all_tests(self) -> Dict[str, ABTest]:
        """Get all active tests."""
        return {k: v for k, v in self.tests.items() if v.is_active}
    
    def end_test(self, test_id: str) -> None:
        """End a test."""
        if test_id in self.tests:
            self.tests[test_id].is_active = False
            logger.info(f"[ABTestManager] Test ended: {test_id}")
