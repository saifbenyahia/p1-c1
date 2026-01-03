# crypto/utils.py - CORRECT VERSION
import re
from typing import List, Dict


def clean_text(text: str, keep_punctuation: bool = False) -> str:
    """Clean text by removing unwanted characters."""
    if keep_punctuation:
        cleaned = re.sub(r'[^a-zA-Z0-9\s.,!?;:\'\"-]', '', text)
    else:
        cleaned = re.sub(r'[^a-zA-Z\s]', '', text)
    
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()


def validate_text(text: str, min_length: int = 10) -> bool:
    """Validate if text is suitable for analysis."""
    if not isinstance(text, str):
        return False
    if len(text.strip()) < min_length:
        return False
    if not any(char.isalpha() for char in text):
        return False
    return True


def calculate_letter_frequency(text: str) -> Dict[str, float]:
    """Calculate letter frequencies in text."""
    letters = [char.lower() for char in text if char.isalpha()]
    
    if not letters:
        return {}
    
    total = len(letters)
    frequencies = {}
    
    for letter in set(letters):
        count = letters.count(letter)
        frequencies[letter] = (count / total) * 100
    
    return dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True))


def split_into_words(text: str) -> List[str]:
    """Split text into words."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return [word.lower() for word in words]