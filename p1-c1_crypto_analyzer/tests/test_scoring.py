import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from analysis.scorer import TextScorer


class TestTextScorer(unittest.TestCase):
    
    def setUp(self):
        self.scorer = TextScorer()
    
    def test_score_stopwords(self):
        english_text = "The quick brown fox jumps over the lazy dog"
        random_text = "Xyzpd qwlk rtvb nmgh sdfjkc vbncz"
        
        english_score = self.scorer.score_stopwords(english_text)
        random_score = self.scorer.score_stopwords(random_text)
        
        self.assertGreater(english_score, random_score)
        self.assertTrue(0 <= english_score <= 100)
        self.assertTrue(0 <= random_score <= 100)
    
    def test_score_frequency(self):
        english_text = "This is a proper English sentence with common words"
        random_text = "Qwertyuiopasdfghjklzxcvbnm"
        
        english_score = self.scorer.score_frequency(english_text)
        random_score = self.scorer.score_frequency(random_text)
        
        self.assertGreater(english_score, random_score)
    
    def test_combined_score(self):
        text = "The encryption algorithm works perfectly"
        score = self.scorer.combined_score(text)
        
        self.assertTrue(0 <= score <= 100)
        self.assertIsInstance(score, float)
    
    def test_empty_text(self):
        score = self.scorer.combined_score("")
        self.assertEqual(score, 0.0)
    
    def test_extract_words(self):
        text = "Hello, World! This is a test."
        words = self.scorer._extract_words(text)
        
        expected = ['hello', 'world', 'this', 'is', 'a', 'test']
        self.assertEqual(words, expected)


if __name__ == "__main__":
    unittest.main()