# create_test_file.py
import sys
sys.path.append('.')

from crypto.caesar import CaesarCipher

# Create test message
plaintext = """This is a test message for the Caesar cipher breaker.
The secret flag is: FLAG{test_success_123}
This project demonstrates intelligent cryptanalysis.
The quick brown fox jumps over the lazy dog."""

# Encrypt with key 13 (ROT13)
key = 13
ciphertext = CaesarCipher.encrypt(plaintext, key)

# Save to file
with open('test_message.txt', 'w') as f:
    f.write(ciphertext)

print("✅ Test ciphertext created!")
print(f"Key used: {key}")
print(f"File: test_message.txt")
print(f"\nCiphertext preview:")
print("-" * 40)
print(ciphertext[:100] + "...")
print("-" * 40)
print("\nTo decrypt, run:")
print("python cli/crack_caesar.py --input test_message.txt")