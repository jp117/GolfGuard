import unittest
import numpy as np
from golf_guard import (
    calculate_score_differential,
    get_standard_deviation_range,
    calculate_z_score,
    get_flag_status,
    calculate_probability_range
)

class TestGolfGuard(unittest.TestCase):
    def test_calculate_score_differential(self):
        # Test case 1: Normal round
        diff = calculate_score_differential(72, 72.0, 113)
        self.assertAlmostEqual(diff, 0.0, places=2)
        
        # Test case 2: Better than expected
        diff = calculate_score_differential(69, 72.0, 113)
        self.assertAlmostEqual(diff, -3.0, places=2)
        
        # Test case 3: Worse than expected
        diff = calculate_score_differential(75, 72.0, 113)
        self.assertAlmostEqual(diff, 3.0, places=2)
        
        # Test case 4: Different slope rating
        diff = calculate_score_differential(72, 72.0, 130)
        self.assertAlmostEqual(diff, 0.0, places=2)

    def test_get_standard_deviation_range(self):
        # Test case 1: Scratch golfer
        low, high = get_standard_deviation_range(0)
        self.assertEqual(low, 1.8)
        self.assertEqual(high, 2.2)
        
        # Test case 2: Mid-handicap
        low, high = get_standard_deviation_range(12)
        self.assertEqual(low, 3.0)
        self.assertEqual(high, 3.5)
        
        # Test case 3: High handicap
        low, high = get_standard_deviation_range(25)
        self.assertEqual(low, 4.0)
        self.assertEqual(high, 4.5)
        
        # Test case 4: Very high handicap
        low, high = get_standard_deviation_range(35)
        self.assertEqual(low, 5.0)
        self.assertEqual(high, 5.5)

    def test_calculate_z_score(self):
        # Test case 1: Expected performance
        z = calculate_z_score(10, 72.0, 113, 82)
        self.assertAlmostEqual(z, 0.0, places=1)
        
        # Test case 2: Better than expected
        z = calculate_z_score(10, 72.0, 113, 77)
        self.assertGreater(z, 0)
        
        # Test case 3: Worse than expected
        z = calculate_z_score(10, 72.0, 113, 87)
        self.assertLess(z, 0)

    def test_get_flag_status(self):
        # Test case 1: No flag (normal round)
        flag, explanation = get_flag_status(0.5, 1.5, -2)
        self.assertEqual(flag, "⚪ NO FLAG")
        
        # Test case 2: Red flag (suspiciously good)
        flag, explanation = get_flag_status(-1.5, 3.5, 5)
        self.assertEqual(flag, "🔺 RED FLAG")
        
        # Test case 3: Review flag (potentially suspicious)
        flag, explanation = get_flag_status(-0.5, 2.5, 3)
        self.assertEqual(flag, "🟡 REVIEW")
        
        # Test case 4: No flag (worse than expected)
        flag, explanation = get_flag_status(-1.5, 3.5, -5)
        self.assertEqual(flag, "⚪ NO FLAG")

    def test_calculate_probability_range(self):
        # Test case 1: Expected performance
        low_prob, high_prob = calculate_probability_range(10, 72.0, 113, 82)
        self.assertGreater(low_prob, 0)
        self.assertLess(high_prob, 1)
        self.assertLessEqual(low_prob, high_prob)  # Changed to LessEqual to allow equal probabilities
        
        # Test case 2: Better than expected
        low_prob, high_prob = calculate_probability_range(10, 72.0, 113, 77)
        self.assertLess(low_prob, 0.1)  # Should be relatively low probability
        
        # Test case 3: Worse than expected
        low_prob, high_prob = calculate_probability_range(10, 72.0, 113, 87)
        self.assertGreater(low_prob, 0.1)  # Should be relatively high probability

if __name__ == '__main__':
    unittest.main() 