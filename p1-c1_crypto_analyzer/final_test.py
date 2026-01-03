# debug_test.py
import sys
import os

PROJECT_ROOT = r"C:\Users\User\OneDrive\Bureau\p1-c1_crypto_analyzer"
sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

from crypto.caesar import CaesarCipher
from analysis.combined_analyzer import CombinedAnalyzer

print("🔍 DÉBUGAGE TEST_MESSAGE.TXT")
print("=" * 60)

# Lire le fichier
with open('test_message.txt', 'r') as f:
    ciphertext = f.read()

print(f"Contenu brut ({len(ciphertext)} caractères):")
print(repr(ciphertext))  # montre les caractères spéciaux
print()

# Analyser
analyzer = CombinedAnalyzer()
results = analyzer.analyze_caesar(ciphertext, top_n=3)

best = results['best_solution']
print(f"Clé trouvée: {best['key']}")
print(f"Score: {best['score']}")
print(f"Texte déchiffré (repr): {repr(best['plaintext'])}")
print(f"Texte déchiffré (normal): {best['plaintext']}")

# Vérifier chaque clé
print("\n🔑 TEST DE TOUTES LES CLÉS:")
for key in range(1, 26):
    decrypted = CaesarCipher.decrypt(ciphertext, key)
    if "flag" in decrypted.lower() or "FLAG" in decrypted:
        print(f"Clé {key}: {decrypted[:50]}...")