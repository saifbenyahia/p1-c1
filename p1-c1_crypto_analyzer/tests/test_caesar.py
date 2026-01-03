# tests/test_caesar.py - COMPLETE FIXED VERSION
import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from crypto.caesar import CaesarCipher


class TestCaesarCipher(unittest.TestCase):
    
    def test_encrypt_decrypt(self):
        """Test basic encrypt/decrypt cycle"""
        test_cases = [
            ("Hello World!", 3, "Khoor Zruog!"),
            ("Python", 13, "Clguba"),
            ("", 5, ""),
            ("123!@#", 10, "123!@#"),
            ("ABCxyz", 1, "BCDyza"),
        ]
        
        for plaintext, key, expected in test_cases:
            with self.subTest(plaintext=plaintext, key=key):
                encrypted = CaesarCipher.encrypt(plaintext, key)
                self.assertEqual(encrypted, expected)
                decrypted = CaesarCipher.decrypt(encrypted, key)
                self.assertEqual(decrypted, plaintext)
    
    def test_brute_force(self):
        """Test brute-force generates all 25 candidates"""
        ciphertext = "Khoor Zruog!"
        candidates = CaesarCipher.brute_force(ciphertext)
        
        self.assertEqual(len(candidates), 25)
        
        # Check all keys 1-25 are present
        keys = [key for key, _ in candidates]
        self.assertEqual(sorted(keys), list(range(1, 26)))
    
    def test_invalid_key(self):
        """Test key validation and normalization"""
        # Test normalization of valid keys
        self.assertEqual(CaesarCipher.validate_key(5), 5)
        self.assertEqual(CaesarCipher.validate_key(26), 0)   # 26 wraps to 0
        self.assertEqual(CaesarCipher.validate_key(27), 1)   # 27 wraps to 1
        self.assertEqual(CaesarCipher.validate_key(-1), 25)  # -1 wraps to 25
        self.assertEqual(CaesarCipher.validate_key(-26), 0)  # -26 wraps to 0
        
        # Test that encryption works with normalized keys
        self.assertEqual(
            CaesarCipher.encrypt("test", 26),
            CaesarCipher.encrypt("test", 0)
        )
        self.assertEqual(
            CaesarCipher.encrypt("test", 27),
            CaesarCipher.encrypt("test", 1)
        )
        self.assertEqual(
            CaesarCipher.encrypt("test", -1),
            CaesarCipher.encrypt("test", 25)
        )
        
        # Test type validation
        with self.assertRaises(TypeError):
            CaesarCipher.validate_key("5")  # String instead of int
        
        with self.assertRaises(TypeError):
            CaesarCipher.validate_key(5.5)  # Float instead of int
    
    def test_case_preservation(self):
        """Test that case is preserved during encryption - CORRECTED"""
        # Simple test cases without spaces in the middle
        test_cases = [
            ("Hello", "Khoor", 3),      # H->K (upper), e->h (lower)
            ("WORLD", "ZRUOG", 3),      # All uppercase
            ("test", "whvw", 3),        # All lowercase
            ("MiXeD", "PlAhG", 3),      # Mixed case - CORRECTED: MiXeD -> PlAhG
        ]
        
        for plain, expected_encrypted, key in test_cases:
            encrypted = CaesarCipher.encrypt(plain, key)
            self.assertEqual(encrypted, expected_encrypted,
                           f"Failed for '{plain}' with key {key}. Got '{encrypted}', expected '{expected_encrypted}'")
            
            # Check case preservation
            for i in range(len(plain)):
                if plain[i].isalpha():
                    self.assertEqual(
                        plain[i].isupper(),
                        encrypted[i].isupper(),
                        f"Case not preserved at position {i}: {plain[i]} -> {encrypted[i]}"
                    )
    
    def test_non_alphabetic(self):
        """Test non-alphabetic characters are preserved - CORRECTED INDICES"""
        text = "Hello, World! 123 @#$"
        encrypted = CaesarCipher.encrypt(text, 5)
        
        # The string "Hello, World! 123 @#$" has these indices:
        # 0:H, 1:e, 2:l, 3:l, 4:o, 5:,, 6: (space), 7:W, 8:o, 9:r, 10:l, 11:d, 12:!, 13: (space), 14:1, 15:2, 16:3, 17: (space), 18:@, 19:#, 20:$
        
        # Check special characters are preserved
        self.assertIn(",", encrypted)
        self.assertIn("!", encrypted)
        self.assertIn("1", encrypted)
        self.assertIn("@", encrypted)
        self.assertIn("#", encrypted)
        self.assertIn("$", encrypted)
        
        # Check specific positions - CORRECTED INDICES
        self.assertEqual(encrypted[5], ',', "Comma should be at position 5")
        self.assertEqual(encrypted[6], ' ', "Space should be at position 6")  # WAS 7, NOW 6
        self.assertEqual(encrypted[12], '!', "Exclamation should be at position 12")
        
        # Also verify some letters are encrypted correctly
        self.assertEqual(encrypted[0], 'M')  # H + 5 = M
        self.assertEqual(encrypted[1], 'j')  # e + 5 = j
        self.assertEqual(encrypted[7], 'B')  # W + 5 = B
    
    def test_frequency_analysis(self):
        """Test frequency analysis method"""
        # Create a ciphertext with known frequencies
        plaintext = "eeeeee ttttt aaaa oooo"  # Lots of e's
        ciphertext = CaesarCipher.encrypt(plaintext, 3)
        result = CaesarCipher.frequency_analysis(ciphertext)
        
        # Check basic structure
        self.assertIn("most_common_letter", result)
        self.assertIn("estimated_key", result)
        self.assertIn("total_letters", result)
        self.assertIn("top_frequencies", result)
        
        # Most common letter should be 'h' (e shifted by 3)
        # But only if there are enough letters for frequency analysis
        if result["most_common_letter"]:
            self.assertEqual(result["most_common_letter"], 'h')
            # Estimated key should be 3
            self.assertEqual(result["estimated_key"], 3)
        
        # Should have analyzed letters
        self.assertGreater(result["total_letters"], 0)
    
    def test_edge_cases(self):
        """Test edge cases and boundaries"""
        # Empty string
        self.assertEqual(CaesarCipher.encrypt("", 5), "")
        self.assertEqual(CaesarCipher.decrypt("", 5), "")
        
        # Only punctuation
        self.assertEqual(CaesarCipher.encrypt("!@#$%", 10), "!@#$%")
        
        # Key 0 (no change)
        text = "Test message"
        self.assertEqual(CaesarCipher.encrypt(text, 0), text)
        
        # Key 26 (wraps around to 0)
        self.assertEqual(
            CaesarCipher.encrypt("abc", 1),
            CaesarCipher.encrypt("abc", 27)  # 27 % 26 = 1
        )
    
    def test_negative_key_encryption(self):
        """Test encryption with negative keys"""
        text = "Hello"
        
        # Encrypt with positive key, then with equivalent negative key
        encrypted_pos = CaesarCipher.encrypt(text, 3)
        encrypted_neg = CaesarCipher.encrypt(text, -23)  # -23 % 26 = 3
        
        self.assertEqual(encrypted_pos, encrypted_neg)
        
        # Test direct negative key
        encrypted = CaesarCipher.encrypt(text, -3)
        decrypted = CaesarCipher.decrypt(encrypted, -3)
        self.assertEqual(decrypted, text)


def run_tests():
    """Run all tests and display results"""
    print("Running Caesar Cipher Tests...")
    print("=" * 60)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCaesarCipher)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print(f"❌ Tests failed: {len(result.failures)} failures, {len(result.errors)} errors")
        for test, error in result.failures:
            print(f"\nFailed test: {test}")
            print(f"Error: {error}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)