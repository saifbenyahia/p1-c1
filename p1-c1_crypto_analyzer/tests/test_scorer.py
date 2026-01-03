# tests/test_scorer.py - COMPLETE TEST FILE
import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from analysis.scorer import TextScorer


class TestTextScorer(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixture."""
        self.scorer = TextScorer()
    
    def test_score_stopwords(self):
        """Test stopwords scoring."""
        # English text with stopwords
        english_text = "The quick brown fox jumps over the lazy dog"
        
        # Random text without stopwords
        random_text = "Xyzpd qwlk rtvb nmgh sdfjkc vbncz"
        
        english_score = self.scorer.score_stopwords(english_text)
        random_score = self.scorer.score_stopwords(random_text)
        
        # English should score higher
        self.assertGreater(english_score, random_score)
        
        # Scores should be in 0-100 range
        self.assertGreaterEqual(english_score, 0.0)
        self.assertLessEqual(english_score, 100.0)
        self.assertGreaterEqual(random_score, 0.0)
        self.assertLessEqual(random_score, 100.0)
        
        # Test empty text
        empty_score = self.scorer.score_stopwords("")
        self.assertEqual(empty_score, 0.0)
    
    def test_score_dictionary(self):
        """Test dictionary word scoring."""
        # Text with dictionary words
        good_text = "Hello world this is a test message"
        
        # Text with non-dictionary words
        bad_text = "Xyzpd qwlk rtvb nmgh sdfjkc"
        
        good_score = self.scorer.score_dictionary(good_text)
        bad_score = self.scorer.score_dictionary(bad_text)
        
        # Good text should score higher
        self.assertGreater(good_score, bad_score)
        
        # Scores should be in 0-100 range
        self.assertGreaterEqual(good_score, 0.0)
        self.assertLessEqual(good_score, 100.0)
        self.assertGreaterEqual(bad_score, 0.0)
        self.assertLessEqual(bad_score, 100.0)
    
    def test_score_frequency(self):
        """Test letter frequency scoring."""
        # English-like text
        english_text = "This is a proper English sentence with common letters"
        
        # Text with uniform letter distribution (low frequency score)
        uniform_text = "Qwertyuiopasdfghjklzxcvbnm" * 2
        
        english_score = self.scorer.score_frequency(english_text)
        uniform_score = self.scorer.score_frequency(uniform_text)
        
        # English should score higher
        self.assertGreater(english_score, uniform_score)
        
        # Scores should be in 0-100 range
        self.assertGreaterEqual(english_score, 0.0)
        self.assertLessEqual(english_score, 100.0)
        self.assertGreaterEqual(uniform_score, 0.0)
        self.assertLessEqual(uniform_score, 100.0)
        
        # Test with very short text
        short_score = self.scorer.score_frequency("Hi")
        self.assertGreaterEqual(short_score, 0.0)
        self.assertLessEqual(short_score, 100.0)
    
    def test_score_bigrams(self):
        """Test bigram scoring."""
        # Text with common English bigrams
        english_text = "The quick brown fox jumps over the lazy dog"
        
        # Text with rare bigrams
        rare_text = "Xq zv bp cw dt eu fv gw hx iy jz"
        
        english_score = self.scorer.score_bigrams(english_text)
        rare_score = self.scorer.score_bigrams(rare_text)
        
        # English should score higher
        self.assertGreater(english_score, rare_score)
        
        # Scores should be in 0-100 range
        self.assertGreaterEqual(english_score, 0.0)
        self.assertLessEqual(english_score, 100.0)
        self.assertGreaterEqual(rare_score, 0.0)
        self.assertLessEqual(rare_score, 100.0)
        
        # Test with very short text
        short_score = self.scorer.score_bigrams("A")
        self.assertEqual(short_score, 0.0)
        
        two_char_score = self.scorer.score_bigrams("Th")
        self.assertGreaterEqual(two_char_score, 0.0)
        self.assertLessEqual(two_char_score, 100.0)
    
    def test_score_entropy(self):
        """Test entropy scoring."""
        # Normal English text (entropy ~4.07)
        english_text = "This is a sample text for testing entropy calculation"
        
        # Repeated text (low entropy)
        repeated_text = "AAAAA BBBBB CCCCC DDDDD EEEEE"
        
        # Random letters (high entropy)
        random_text = "QwErTyUiOpAsDfGhJkLzXcVbNm"
        
        english_score = self.scorer.score_entropy(english_text)
        repeated_score = self.scorer.score_entropy(repeated_text)
        random_score = self.scorer.score_entropy(random_text)
        
        # English should have good score (close to 4.07)
        # Repeated text should have lower score
        # Very random text might also have lower score
        
        # All scores should be in 0-100 range
        self.assertGreaterEqual(english_score, 0.0)
        self.assertLessEqual(english_score, 100.0)
        self.assertGreaterEqual(repeated_score, 0.0)
        self.assertLessEqual(repeated_score, 100.0)
        self.assertGreaterEqual(random_score, 0.0)
        self.assertLessEqual(random_score, 100.0)
    
    def test_combined_score(self):
        """Test combined scoring."""
        # Good English text
        good_text = "The Caesar cipher is a simple encryption method used since ancient times"
        
        # Random text
        random_text = "Zpqr stuv wxyz abcd efgh ijkl mnop"
        
        good_score = self.scorer.combined_score(good_text)
        random_score = self.scorer.combined_score(random_text)
        
        # Good text should score higher
        self.assertGreater(good_score, random_score)
        
        # Scores should be in 0-100 range
        self.assertGreaterEqual(good_score, 0.0)
        self.assertLessEqual(good_score, 100.0)
        self.assertGreaterEqual(random_score, 0.0)
        self.assertLessEqual(random_score, 100.0)
        
        # Test with custom weights
        custom_weights = {
            'stopwords': 0.5,
            'dictionary': 0.3,
            'frequency': 0.1,
            'bigrams': 0.1,
            'entropy': 0.0
        }
        
        custom_score = self.scorer.combined_score(good_text, custom_weights)
        self.assertGreaterEqual(custom_score, 0.0)
        self.assertLessEqual(custom_score, 100.0)
    
    def test_extract_words(self):
        """Test word extraction."""
        text = "Hello, World! This is a test-text with punctuation."
        words = self.scorer._extract_words(text)
        
        expected = ['hello', 'world', 'this', 'is', 'a', 'test', 'text', 'with', 'punctuation']
        self.assertEqual(words, expected)
        
        # Test with only punctuation
        punctuation_words = self.scorer._extract_words("!@#$%")
        self.assertEqual(punctuation_words, [])
        
        # Test empty string
        empty_words = self.scorer._extract_words("")
        self.assertEqual(empty_words, [])
    
    def test_analyze_text(self):
        """Test comprehensive text analysis."""
        text = "The quick brown fox jumps over the lazy dog"
        analysis = self.scorer.analyze_text(text)
        
        # Should return all score types
        expected_keys = {'stopwords', 'dictionary', 'frequency', 'bigrams', 'entropy', 'combined'}
        self.assertEqual(set(analysis.keys()), expected_keys)
        
        # All scores should be in 0-100 range
        for method, score in analysis.items():
            self.assertGreaterEqual(score, 0.0, f"{method} score below 0: {score}")
            self.assertLessEqual(score, 100.0, f"{method} score above 100: {score}")
    
    def test_different_text_types(self):
        """Test scoring with different types of text."""
        test_cases = [
            ("Perfect English text with common words and structure", "high"),
            ("Mixed text with some English xyzpd random qwlk", "medium"),
            ("Xyzpd qwlk rtvb nmgh completely random", "low"),
            ("", "empty"),
            ("12345 !@#$% only numbers and symbols", "symbols"),
        ]
        
        for text, text_type in test_cases:
            with self.subTest(text_type=text_type):
                scores = self.scorer.analyze_text(text)
                
                # Check all scores exist
                self.assertIn('combined', scores)
                
                # Check score ranges
                for method, score in scores.items():
                    self.assertGreaterEqual(score, 0.0)
                    self.assertLessEqual(score, 100.0)
    
    def test_scoring_consistency(self):
        """Test that scoring is consistent for same input."""
        text = "Consistent testing is important for reliability"
        
        # Get scores multiple times
        scores1 = self.scorer.analyze_text(text)
        scores2 = self.scorer.analyze_text(text)
        
        # Should be exactly the same (allowing for floating point)
        for method in scores1.keys():
            self.assertAlmostEqual(scores1[method], scores2[method], places=5,
                                 msg=f"Scores for {method} not consistent")


def run_tests():
    """Run all scorer tests."""
    print("Running TextScorer Tests...")
    print("=" * 60)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTextScorer)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ All TextScorer tests passed!")
    else:
        print(f"❌ Tests failed: {len(result.failures)} failures, {len(result.errors)} errors")
        for test, error in result.failures:
            print(f"\nFailed test: {test}")
            print(f"Error: {error}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)