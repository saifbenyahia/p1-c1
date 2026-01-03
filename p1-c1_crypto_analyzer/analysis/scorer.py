# analysis/scorer.py - COMPLETE
import string
import math
from collections import Counter
from typing import Dict, List, Optional
from pathlib import Path


class TextScorer:
    """Scores text based on linguistic features to detect English plaintext."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.stopwords = self._load_stopwords()
        self.dictionary = self._load_dictionary()
        
        # English letter frequencies (percentages)
        self.english_frequencies = {
            'e': 12.02, 't': 9.10, 'a': 8.12, 'o': 7.68, 'i': 7.31,
            'n': 6.95, 's': 6.28, 'r': 6.02, 'h': 5.92, 'd': 4.32,
            'l': 3.98, 'u': 2.88, 'c': 2.71, 'm': 2.61, 'f': 2.30,
            'y': 2.11, 'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49,
            'v': 1.11, 'k': 0.69, 'x': 0.17, 'q': 0.11, 'j': 0.10, 'z': 0.07
        }
        
        # Common English bigrams
        self.common_bigrams = {
            'th', 'he', 'in', 'er', 'an', 're', 'nd', 'at', 'on', 'nt',
            'ha', 'es', 'st', 'en', 'ed', 'to', 'it', 'ou', 'ea', 'hi',
            'is', 'or', 'ti', 'as', 'te', 'et', 'ng', 'of', 'al', 'de',
            'se', 'le', 'sa', 'si', 'ar', 've', 'ra', 'ld', 'ur'
        }
    
    def _load_stopwords(self) -> set:
        """Load stopwords from file."""
        stopwords_file = self.data_dir / "stopwords_en.txt"
        if stopwords_file.exists():
            try:
                with open(stopwords_file, 'r', encoding='utf-8') as f:
                    return {line.strip().lower() for line in f if line.strip()}
            except:
                pass
        
        # Fallback stopwords
        return {
            'the', 'and', 'to', 'of', 'a', 'in', 'that', 'is', 'was',
            'he', 'for', 'it', 'with', 'as', 'his', 'on', 'be', 'at',
            'by', 'i', 'this', 'had', 'not', 'are', 'but', 'from',
            'or', 'have', 'an', 'they', 'which', 'one', 'you', 'were',
            'her', 'all', 'she', 'there', 'would', 'their', 'we', 'him'
        }
    
    def _load_dictionary(self) -> set:
        """Load dictionary words from file."""
        dict_file = self.data_dir / "words_en.txt"
        if dict_file.exists():
            try:
                with open(dict_file, 'r', encoding='utf-8') as f:
                    return {line.strip().lower() for line in f if line.strip()}
            except:
                pass
        
        # Fallback dictionary
        return {
            'hello', 'world', 'test', 'message', 'text', 'analysis',
            'cipher', 'encryption', 'decryption', 'key', 'secret',
            'the', 'and', 'that', 'have', 'for', 'not', 'with', 'this',
            'but', 'from', 'they', 'say', 'her', 'she', 'will', 'would',
            'make', 'like', 'time', 'there', 'their', 'what', 'so', 'see',
            'him', 'them', 'when', 'which', 'now', 'then', 'its', 'also'
        }
    
    def score_stopwords(self, text: str) -> float:
        """
        Score based on stopwords count.
        Returns: 0-100
        """
        words = self._extract_words(text)
        if not words:
            return 0.0
        
        stopword_count = sum(1 for word in words if word in self.stopwords)
        percentage = (stopword_count / len(words)) * 100
        
        # Optimal stopword percentage for English is ~20-30%
        optimal = 25.0
        score = 100.0 - min(abs(percentage - optimal) * 3, 100.0)
        
        return max(0.0, min(100.0, score))
    
    def score_dictionary(self, text: str) -> float:
        """
        Score based on dictionary words.
        Returns: 0-100
        """
        words = self._extract_words(text)
        if not words:
            return 0.0
        
        dict_count = sum(1 for word in words if word in self.dictionary)
        score = (dict_count / len(words)) * 100
        
        return max(0.0, min(100.0, score))
    
    def score_frequency(self, text: str) -> float:
        """
        Score based on letter frequency match.
        Returns: 0-100
        """
        letters = [char.lower() for char in text if char.isalpha()]
        if not letters:
            return 0.0
        
        total = len(letters)
        counter = Counter(letters)
        
        # Calculate chi-square like score
        chi_square = 0.0
        for letter, expected_percent in self.english_frequencies.items():
            observed_count = counter.get(letter, 0)
            expected_count = total * (expected_percent / 100)
            
            if expected_count > 0:
                diff = observed_count - expected_count
                chi_square += (diff * diff) / expected_count
        
        # Convert chi-square to score (lower chi-square = better match)
        # Typical English text has chi-square around 150-300 for 26 letters
        if chi_square < 150:
            score = 100.0
        elif chi_square > 1000:
            score = 0.0
        else:
            score = 100.0 - ((chi_square - 150) / 8.5)
        
        return max(0.0, min(100.0, score))
    
    def score_bigrams(self, text: str) -> float:
        """
        Score based on common bigrams.
        Returns: 0-100
        """
        # Clean text: keep only letters and convert to lowercase
        cleaned = ''.join(char.lower() for char in text if char.isalpha())
        
        if len(cleaned) < 2:
            return 0.0
        
        # Count common bigrams
        common_count = 0
        for i in range(len(cleaned) - 1):
            bigram = cleaned[i:i+2]
            if bigram in self.common_bigrams:
                common_count += 1
        
        # Calculate percentage
        total_bigrams = len(cleaned) - 1
        percentage = (common_count / total_bigrams) * 100
        
        # Optimal is around 10-15% for English
        optimal = 12.5
        score = 100.0 - min(abs(percentage - optimal) * 6, 100.0)
        
        return max(0.0, min(100.0, score))
    
    def score_entropy(self, text: str) -> float:
        """
        Score based on character entropy.
        English has entropy ~4.07 bits/character.
        Returns: 0-100
        """
        letters = [char.lower() for char in text if char.isalpha()]
        
        if len(letters) < 10:  # Need enough text for meaningful entropy
            return 50.0
        
        total = len(letters)
        counter = Counter(letters)
        
        # Calculate Shannon entropy
        entropy = 0.0
        for count in counter.values():
            probability = count / total
            entropy -= probability * math.log2(probability)
        
        # English entropy is ~4.07 bits/character
        optimal_entropy = 4.07
        entropy_diff = abs(entropy - optimal_entropy)
        
        # Convert to score
        if entropy_diff < 0.5:
            score = 100.0
        elif entropy_diff > 2.0:
            score = 0.0
        else:
            score = 100.0 - (entropy_diff * 50)
        
        return max(0.0, min(100.0, score))
    
    def combined_score(self, text: str, weights: Optional[Dict[str, float]] = None) -> float:
        """
        Combined score using all methods with weights.
        Returns: 0-100
        """
        if weights is None:
            weights = {
                'stopwords': 0.30,    # Most important for short texts
                'dictionary': 0.25,   # Important for word recognition
                'frequency': 0.20,    # Good for longer texts
                'bigrams': 0.15,      # Good for text structure
                'entropy': 0.10       # Good for randomness detection
            }
        
        # Calculate individual scores
        scores = {
            'stopwords': self.score_stopwords(text),
            'dictionary': self.score_dictionary(text),
            'frequency': self.score_frequency(text),
            'bigrams': self.score_bigrams(text),
            'entropy': self.score_entropy(text)
        }
        
        # Calculate weighted average
        total_weight = sum(weights.values())
        weighted_score = 0.0
        
        for method, weight in weights.items():
            if method in scores:
                weighted_score += scores[method] * weight
        
        # Normalize by total weight
        if total_weight > 0:
            weighted_score /= total_weight
        
        return max(0.0, min(100.0, weighted_score))
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract words from text (letters only, converted to lowercase)."""
        words = []
        current_word = []
        
        for char in text:
            if char.isalpha():
                current_word.append(char.lower())
            elif current_word:
                words.append(''.join(current_word))
                current_word = []
        
        # Add last word if exists
        if current_word:
            words.append(''.join(current_word))
        
        return words
    
    def analyze_text(self, text: str) -> Dict[str, float]:
        """
        Return detailed analysis of text scores.
        """
        return {
            'stopwords': self.score_stopwords(text),
            'dictionary': self.score_dictionary(text),
            'frequency': self.score_frequency(text),
            'bigrams': self.score_bigrams(text),
            'entropy': self.score_entropy(text),
            'combined': self.combined_score(text)
        }