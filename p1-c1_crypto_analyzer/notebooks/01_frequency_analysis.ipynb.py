# Cell 1: Import libraries
import sys
sys.path.append('..')
from crypto.caesar import CaesarCipher
from analysis.scorer import TextScorer
import matplotlib.pyplot as plt
import pandas as pd

# Cell 2: Load sample data
with open('../data/samples/sample_plain.txt', 'r') as f:
    sample_text = f.read()

# Cell 3: Perform frequency analysis
freq = CaesarCipher.frequency_analysis(sample_text)
print("Frequency Analysis Results:")
print(f"Total letters: {freq['total_letters']}")
print(f"Most common letter: {freq['most_common_letter']}")
print(f"Estimated key: {freq['estimated_key']}