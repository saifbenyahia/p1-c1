# crypto/caesar.py - VERSION P1-C1
import string
from typing import List, Tuple, Dict, Any


class CaesarCipher:
    ENGLISH_FREQUENCIES = {
        'e': 12.02, 't': 9.10, 'a': 8.12, 'o': 7.68, 'i': 7.31,
        'n': 6.95, 's': 6.28, 'r': 6.02, 'h': 5.92, 'd': 4.32,
        'l': 3.98, 'u': 2.88, 'c': 2.71, 'm': 2.61, 'f': 2.30,
        'y': 2.11, 'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49,
        'v': 1.11, 'k': 0.69, 'x': 0.17, 'q': 0.11, 'j': 0.10, 'z': 0.07
    }
    
    @staticmethod
    def validate_key(key: int) -> int:
        """
        Valide et normalise la clé dans la plage 0-25.
        
        Args:
            key: La clé à valider
            
        Returns:
            Clé normalisée (0-25)
            
        Raises:
            TypeError: Si la clé n'est pas un entier
        """
        if not isinstance(key, int):
            raise TypeError(f"La clé doit être un entier, reçu {type(key)}")
        return key % 26
    
    @staticmethod
    def encrypt(plaintext: str, key: int) -> str:
        """
        Chiffre un texte avec le chiffrement César.
        
        Args:
            plaintext: Texte à chiffrer
            key: Valeur de décalage (n'importe quel entier, sera normalisé)
            
        Returns:
            Texte chiffré
        """
        # Normaliser la clé
        key = CaesarCipher.validate_key(key)
        
        if not plaintext:
            return plaintext
        
        result = []
        for char in plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                original_pos = ord(char) - base
                new_pos = (original_pos + key) % 26
                result.append(chr(new_pos + base))
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def decrypt(ciphertext: str, key: int) -> str:
        """
        Déchiffre un texte chiffré avec César.
        
        Args:
            ciphertext: Texte à déchiffrer
            key: Valeur de décalage utilisée pour le chiffrement
            
        Returns:
            Texte déchiffré
        """
        return CaesarCipher.encrypt(ciphertext, -key)
    
    @staticmethod
    def brute_force(ciphertext: str) -> List[Tuple[int, str]]:
        """
        Génère toutes les hypothèses de déchiffrement possibles.
        Intelligence: teste seulement 25 clés (1-25) car:
        - Clé 0 = pas de chiffrement (inutile)
        - Clé 26 = Clé 0 (redondant)
        
        Args:
            ciphertext: Texte à analyser
            
        Returns:
            Liste de tuples (clé, texte_déchiffré)
        """
        hypotheses = []
        for key in range(1, 26):  # Clés 1 à 25 seulement
            plaintext = CaesarCipher.decrypt(ciphertext, key)
            hypotheses.append((key, plaintext))
        return hypotheses
    
    @staticmethod
    def frequency_analysis(ciphertext: str) -> Dict[str, Any]:
        """
        Effectue une analyse fréquentielle sur le texte chiffré.
        
        Args:
            ciphertext: Texte à analyser
            
        Returns:
            Dictionnaire avec résultats d'analyse
        """
        from collections import Counter
        
        letters = [char.lower() for char in ciphertext if char.isalpha()]
        if not letters:
            return {"error": "Aucune lettre trouvée pour l'analyse"}
        
        total = len(letters)
        counter = Counter(letters)
        sorted_letters = counter.most_common()
        
        most_common = sorted_letters[0][0] if sorted_letters else None
        estimated_key = (ord(most_common) - ord('e')) % 26 if most_common else None
        
        percentages = {
            letter: (count / total) * 100 
            for letter, count in sorted_letters[:10]
        }
        
        return {
            "total_letters": total,
            "most_common_letter": most_common,
            "estimated_key": estimated_key,
            "top_frequencies": dict(sorted_letters[:5]),
            "percentages": percentages
        }


# Fonctions de convenance
def caesar_encrypt(plaintext: str, key: int) -> str:
    """Fonction de convenance pour le chiffrement."""
    return CaesarCipher.encrypt(plaintext, key)


def caesar_decrypt(ciphertext: str, key: int) -> str:
    """Fonction de convenance pour le déchiffrement."""
    return CaesarCipher.decrypt(ciphertext, key)


def brute_force_caesar(ciphertext: str) -> List[Tuple[int, str]]:
    """Fonction de convenance pour l'attaque par brute-force."""
    return CaesarCipher.brute_force(ciphertext)