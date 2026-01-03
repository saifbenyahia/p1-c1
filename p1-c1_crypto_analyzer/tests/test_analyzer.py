import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from analysis.combined_analyzer import CombinedAnalyzer


class TestCombinedAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.analyzer = CombinedAnalyzer()
    
    def test_analyze(self):
        from crypto.caesar import CaesarCipher
        
        plaintext = "This is a secret message for testing the Caesar cipher"
        ciphertext = CaesarCipher.encrypt(plaintext, 19)
        
        results = self.analyzer.analyze(ciphertext)
        
        self.assertIn("best_candidate", results)
        self.assertIn("top_candidates", results)
        self.assertIn("frequency_analysis", results)
        
        best = results["best_candidate"]
        self.assertIsNotNone(best)
        self.assertEqual(best["key"], 19)
        self.assertEqual(best["plaintext"], plaintext)
    
    def test_confidence_levels(self):
        test_cases = [
            (95, "Très Élevée"),
            (75, "Élevée"),
            (55, "Moyenne"),
            (25, "Faible"),
            (5, "Très Faible"),
        ]
        
        for score, expected in test_cases:
            confidence = self.analyzer._get_confidence_level(score)
            self.assertEqual(confidence, expected)
    
    def test_find_flag(self):
        results = {
            "top_candidates": [
                {"plaintext": "Normal text here"},
                {"plaintext": "The secret is FLAG{secret123}"},
                {"plaintext": "More text here"},
            ]
        }
        
        flag = self.analyzer.find_flag(results)
        self.assertEqual(flag, "FLAG{secret123}")
    
    def test_no_flag_found(self):
        results = {
            "top_candidates": [
                {"plaintext": "Normal text here"},
                {"plaintext": "No flag in this text"},
            ]
        }
        
        flag = self.analyzer.find_flag(results)
        self.assertEqual(flag, "")


if __name__ == "__main__":
    unittest.main()