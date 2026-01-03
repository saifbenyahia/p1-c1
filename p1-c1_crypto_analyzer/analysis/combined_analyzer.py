# analysis/combined_analyzer.py - VERSION CORRIGÉE P1-C1
import time
import json
from typing import Dict, List, Any, Optional

from analysis.scorer import TextScorer
from crypto.caesar import CaesarCipher


class CombinedAnalyzer:
    """
    Cryptanalyse intelligente combinant multiples techniques.
    Déchiffre automatiquement le chiffrement César avec scoring avancé.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialise l'analyseur intelligent.
        
        Args:
            data_dir: Répertoire contenant les fichiers de données
        """
        self.scorer = TextScorer(data_dir)
        
        # Pondérations intelligentes pour le scoring combiné
        self.scoring_weights = {
            'stopwords': 0.30,    # Détection immédiate de l'anglais
            'dictionary': 0.25,   # Validation des mots existants
            'frequency': 0.20,    # Analyse statistique des lettres
            'bigrams': 0.15,      # Structure linguistique
            'entropy': 0.10       # Détection de bruit/aléatoire
        }
    
    def analyze_caesar(self, ciphertext: str, top_n: int = 5) -> Dict[str, Any]:
        """
        Analyse et déchiffre automatiquement un chiffrement César.
        
        Args:
            ciphertext: Texte chiffré à analyser
            top_n: Nombre de meilleures solutions à retourner
            
        Returns:
            Dictionnaire avec résultats complets d'analyse intelligente
        """
        start_time = time.time()
        
        # Générer toutes les hypothèses de déchiffrement (25 possibilités)
        hypotheses = CaesarCipher.brute_force(ciphertext)
        
        # Évaluer chaque hypothèse avec scoring intelligent
        evaluated_hypotheses = []
        for key, plaintext in hypotheses:
            score = self.scorer.combined_score(plaintext, self.scoring_weights)
            confidence = self._get_confidence_level(score)
            
            evaluated_hypotheses.append({
                'key': key,
                'plaintext': plaintext,
                'score': round(score, 2),
                'confidence': confidence,
                'preview': plaintext[:120] + "..." if len(plaintext) > 120 else plaintext
            })
        
        # Trier par score (décroissant) - décision intelligente
        evaluated_hypotheses.sort(key=lambda x: x['score'], reverse=True)
        
        # Meilleure solution identifiée
        best_solution = evaluated_hypotheses[0] if evaluated_hypotheses else None
        
        # Analyse fréquentielle pour comparaison
        freq_analysis = CaesarCipher.frequency_analysis(ciphertext)
        
        analysis_time = time.time() - start_time
        
        # Calculer des statistiques intelligentes
        scores = [h['score'] for h in evaluated_hypotheses]
        score_range = (min(scores), max(scores)) if scores else (0, 0)
        
        return {
            'best_solution': best_solution,
            'top_solutions': evaluated_hypotheses[:top_n],
            'frequency_analysis': freq_analysis,
            'statistics': {
                'analysis_time_seconds': round(analysis_time, 3),
                'total_hypotheses': len(hypotheses),
                'score_range': score_range,
                'mean_score': sum(scores)/len(scores) if scores else 0,
                'std_deviation': self._calculate_std_dev(scores) if len(scores) > 1 else 0,
                'confidence_gap': scores[0] - scores[1] if len(scores) > 1 else 0
            },
            'metadata': {
                'ciphertext_length': len(ciphertext),
                'alphabetic_chars': sum(1 for c in ciphertext if c.isalpha()),
                'analysis_date': time.strftime("%Y-%m-%d %H:%M:%S"),
                'scoring_methods': list(self.scoring_weights.keys()),
                'weights_used': self.scoring_weights
            }
        }
    
    def analyze_text_complexity(self, text: str) -> Dict[str, Any]:
        """
        Analyse la complexité linguistique d'un texte.
        EXEMPLE INTELLIGENT P1-C1: Prise de décision contextuelle.
        
        Args:
            text: Texte à analyser
            
        Returns:
            Analyse détaillée de la complexité avec décisions intelligentes
        """
        # Analyser différentes caractéristiques linguistiques
        words = self.scorer._extract_words(text)
        word_count = len(words)
        letter_count = sum(1 for c in text if c.isalpha())
        
        # Valeurs par défaut
        result = {
            'word_count': word_count,
            'letter_count': letter_count,
            'analysis_type': 'standard',
            'reliability': 'moyenne',
            'recommendation': 'Analyse standard',
            'probable_text_type': 'texte générique',
            'analysis_focus': 'méthodes équilibrées',
            'vocabulary_assessment': 'standard',
            'info_density': 0.0,
            'is_analyzable': word_count >= 5
        }
        
        # DÉCISION INTELLIGENTE 1: Adapter l'analyse selon la longueur
        if word_count < 10:
            result.update({
                'analysis_type': "texte_court",
                'reliability': "faible",
                'recommendation': "Texte très court - fiabilité limitée",
                'probable_text_type': "message court",
                'analysis_focus': "stopwords uniquement",
                'vocabulary_assessment': "limité"
            })
        elif word_count < 50:
            result.update({
                'analysis_type': "texte_moyen",
                'reliability': "moyenne",
                'recommendation': "Analyse possible avec pondérations adaptées",
                'probable_text_type': "texte standard",
                'analysis_focus': "stopwords et dictionnaire",
                'vocabulary_assessment': "adéquat"
            })
        else:
            result.update({
                'analysis_type': "texte_long",
                'reliability': "élevée",
                'recommendation': "Analyse complète et fiable",
                'probable_text_type': "texte détaillé",
                'analysis_focus': "toutes les méthodes",
                'vocabulary_assessment': "riche"
            })
        
        # Calculer la densité d'information (lettres/mot)
        if word_count > 0:
            result['info_density'] = round(letter_count / word_count, 2)
        
        return result
    
    def _get_confidence_level(self, score: float) -> str:
        """
        Convertit un score numérique en niveau de confiance lisible.
        Décision intelligente de catégorisation.
        
        Args:
            score: Score de 0 à 100
            
        Returns:
            Niveau de confiance en français
        """
        if score >= 80:
            return "Très Élevée"
        elif score >= 60:
            return "Élevée"
        elif score >= 40:
            return "Moyenne"
        elif score >= 20:
            return "Faible"
        else:
            return "Très Faible"
    
    def _calculate_std_dev(self, scores: List[float]) -> float:
        """
        Calcule l'écart-type des scores pour évaluer la certitude.
        
        Args:
            scores: Liste des scores
            
        Returns:
            Écart-type
        """
        if len(scores) <= 1:
            return 0.0
        
        mean = sum(scores) / len(scores)
        variance = sum((x - mean) ** 2 for x in scores) / len(scores)
        return variance ** 0.5
    
    def _explain_confidence(self, results: dict) -> str:
        """
        Explique intelligemment pourquoi un niveau de confiance est attribué.
        
        Args:
            results: Résultats d'analyse
            
        Returns:
            Explication textuelle
        """
        if not results.get('best_solution'):
            return "Aucune solution trouvée"
        
        best = results['best_solution']
        stats = results['statistics']
        
        explanations = []
        
        if best['score'] >= 80:
            explanations.append("Score très élevé (>80)")
        elif best['score'] >= 60:
            explanations.append("Score élevé (60-80)")
        
        if stats.get('confidence_gap', 0) > 20:
            explanations.append("Grand écart avec la 2ème solution")
        elif stats.get('confidence_gap', 0) > 10:
            explanations.append("Écart significatif avec la 2ème solution")
        
        if stats.get('std_deviation', 0) > 15:
            explanations.append("Forte dispersion des scores → solution claire")
        
        return "; ".join(explanations) if explanations else "Score moyen sans caractéristique distinctive"
    
    def intelligent_decision_report(self, ciphertext: str) -> Dict[str, Any]:
        """
        Génère un rapport complet des décisions intelligentes prises.
        EXCLUSIF P1-C1 - Démonstration d'analyse contextuelle.
        
        Args:
            ciphertext: Texte chiffré
            
        Returns:
            Rapport détaillé des décisions intelligentes
        """
        # Analyse standard
        results = self.analyze_caesar(ciphertext)
        
        # Analyse de complexité
        complexity = self.analyze_text_complexity(ciphertext)
        
        # Décisions intelligentes combinées
        decisions = {
            'text_complexity_decision': {
                'analysis_type': complexity['analysis_type'],
                'reliability_warning': complexity['reliability'],
                'recommended_action': complexity['recommendation']
            },
            'scoring_strategy': {
                'weights_applied': self.scoring_weights,
                'adjustment_recommended': complexity['analysis_focus'],
                'focus_area': complexity['analysis_focus']
            },
            'confidence_assessment': {
                'score': results['best_solution']['score'] if results['best_solution'] else 0,
                'level': results['best_solution']['confidence'] if results['best_solution'] else "Indéterminé",
                'justification': self._explain_confidence(results) if results['best_solution'] else "Pas de solution fiable"
            },
            'validation_decisions': {
                'is_text_analyzable': complexity['is_analyzable'],
                'needs_calibration': complexity['word_count'] < 20,
                'vocabulary_quality': complexity['vocabulary_assessment']
            }
        }
        
        return decisions
    
    def export_results(self, results: Dict[str, Any], filename: str) -> None:
        """
        Exporte les résultats d'analyse en fichier JSON.
        
        Args:
            results: Résultats d'analyse
            filename: Chemin du fichier de sortie
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    def find_flag(self, results: Dict[str, Any]) -> Optional[str]:
        """
        Recherche intelligente de pattern FLAG{...} dans les résultats.
        
        Args:
            results: Résultats d'analyse
            
        Returns:
            Chaîne du drapeau si trouvé, None sinon
        """
        import re
        
        # Recherche dans les meilleures solutions
        for solution in results.get('top_solutions', []):
            plaintext = solution['plaintext']
            match = re.search(r'FLAG\{([^}]+)\}', plaintext, re.IGNORECASE)
            if match:
                return f"FLAG{{{match.group(1)}}}"  # Format standardisé
        
        return None
    
    def save_flag(self, results: Dict[str, Any], filename: str = "flag.txt") -> bool:
        """
        Sauvegarde le drapeau trouvé dans un fichier.
        
        Args:
            results: Résultats d'analyse
            filename: Nom du fichier de sortie
            
        Returns:
            True si drapeau trouvé et sauvegardé, False sinon
        """
        flag = self.find_flag(results)
        if flag:
            with open(filename, 'w') as f:
                f.write(flag)
            return True
        return False
    
    def compare_methods(self, ciphertext: str) -> Dict[str, Any]:
        """
        Compare différentes méthodes d'analyse.
        Décision intelligente pour optimisation future.
        
        Args:
            ciphertext: Texte chiffré à analyser
            
        Returns:
            Comparaison des méthodes avec recommandations
        """
        hypotheses = CaesarCipher.brute_force(ciphertext)
        
        comparison = []
        for key, plaintext in hypotheses[:10]:  # 10 premières pour rapidité
            analysis = self.scorer.analyze_text(plaintext)
            comparison.append({
                'key': key,
                'plaintext_preview': plaintext[:50] + "..." if len(plaintext) > 50 else plaintext,
                'scores': analysis
            })
        
        # Trier par score combiné
        comparison.sort(key=lambda x: x['scores']['combined'], reverse=True)
        
        # DÉCISION INTELLIGENTE: Identifier la meilleure méthode
        best_solution = comparison[0] if comparison else None
        if best_solution:
            scores = best_solution['scores']
            best_method = max(scores.keys(), key=lambda k: scores[k] if k != 'combined' else 0)
        else:
            best_method = None
        
        return {
            'ciphertext_preview': ciphertext[:100] + "..." if len(ciphertext) > 100 else ciphertext,
            'method_comparison': comparison[:5],
            'best_method': best_method,
            'recommendation': f"Focus sur {best_method}" if best_method else "Analyse non concluante"
        }