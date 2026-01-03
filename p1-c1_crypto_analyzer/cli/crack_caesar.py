#!/usr/bin/env python3
"""
Outil Professionnel de Cryptanalyse César - Projet P1-C1
Système Intelligent de Déchiffrement Automatique
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Chemin absolu vers la racine du projet
PROJECT_ROOT = Path(__file__).parent.parent

# Ajouter la racine du projet au path
sys.path.insert(0, str(PROJECT_ROOT))

from analysis.combined_analyzer import CombinedAnalyzer


def main():
    parser = argparse.ArgumentParser(
        description="Outil de Cryptanalyse César Intelligent - Déchiffrement Automatique P1-C1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation P1-C1:
  %(prog)s --input cipher.txt                    # Analyse basique
  %(prog)s --input cipher.txt --top 10           # Top 10 solutions
  %(prog)s --input cipher.txt --json --output results.json  # Export JSON
  %(prog)s --input cipher.txt --find-flag        # Recherche de drapeau
  %(prog)s --input cipher.txt --verbose          # Sortie détaillée
  %(prog)s --input cipher.txt --complexity       # Analyse de complexité
        """
    )
    
    # Arguments Entrée/Sortie
    input_group = parser.add_argument_group('Entrée/Sortie')
    input_group.add_argument("--input", "-i", required=True,
                           help="Fichier contenant le texte chiffré")
    input_group.add_argument("--output", "-o", 
                           help="Fichier de sortie pour résultats JSON")
    
    # Options d'analyse intelligente
    analysis_group = parser.add_argument_group('Options d\'Analyse Intelligente')
    analysis_group.add_argument("--top", "-t", type=int, default=5,
                              help="Afficher les N meilleures solutions (défaut: 5)")
    analysis_group.add_argument("--find-flag", "-f", action="store_true",
                              help="Rechercher automatiquement le pattern FLAG{...}")
    analysis_group.add_argument("--flag-file", default="flag.txt",
                              help="Fichier pour sauvegarder le drapeau (défaut: flag.txt)")
    analysis_group.add_argument("--complexity", "-c", action="store_true",
                              help="Analyser la complexité linguistique du texte")
    
    # Format de sortie
    output_group = parser.add_argument_group('Format de Sortie')
    output_group.add_argument("--json", action="store_true",
                            help="Sortir les résultats en format JSON")
    output_group.add_argument("--verbose", "-v", action="store_true",
                            help="Afficher les informations d'analyse détaillées")
    output_group.add_argument("--quiet", "-q", action="store_true",
                            help="Supprimer toute sortie sauf les résultats")
    
    args = parser.parse_args()
    
    # Résoudre le chemin du fichier d'entrée
    input_path = Path(args.input)
    if not input_path.is_absolute():
        # Essayer relatif au répertoire courant d'abord
        if not input_path.exists():
            # Essayer relatif à la racine du projet
            input_path = PROJECT_ROOT / args.input
    
    # Lire le fichier d'entrée
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            ciphertext = f.read().strip()
    except FileNotFoundError:
        print(f"❌ Erreur: Fichier '{args.input}' non trouvé aux emplacements:", file=sys.stderr)
        print(f"   • Chemin relatif: {Path(args.input).absolute()}", file=sys.stderr)
        print(f"   • Racine projet: {PROJECT_ROOT}", file=sys.stderr)
        print(f"   • Répertoire courant: {Path.cwd()}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Erreur de lecture: {e}", file=sys.stderr)
        return 1
    
    if not ciphertext:
        print("❌ Erreur: Fichier d'entrée vide", file=sys.stderr)
        return 1
    
    # Initialiser l'analyseur intelligent
    analyzer = CombinedAnalyzer()
    
    if not args.quiet:
        print("🔐 CRYPTANALYSE CÉSAR INTELLIGENTE - P1-C1")
        print("=" * 60)
        print(f"Fichier d'entrée:  {args.input}")
        print(f"Chemin complet:    {input_path}")
        print(f"Longueur texte:    {len(ciphertext)} caractères")
        print(f"Lettres:           {sum(1 for c in ciphertext if c.isalpha())}")
        print(f"Mode d'analyse:    Scoring linguistique intelligent")
        print("-" * 60)
    
    # Analyser la complexité si demandé
    if args.complexity and not args.quiet:
        complexity = analyzer.analyze_text_complexity(ciphertext)
        print(f"\n📊 ANALYSE DE COMPLEXITÉ LINGUISTIQUE:")
        print(f"   Mots détectés:     {complexity.get('word_count', 0)}")
        print(f"   Lettres:           {complexity.get('letter_count', 0)}")
        print(f"   Type d'analyse:    {complexity.get('analysis_type', 'N/A')}")
        print(f"   Fiabilité:         {complexity.get('reliability', 'N/A')}")
        print(f"   Recommandation:    {complexity.get('recommendation', 'N/A')}")
        print(f"   Type texte:        {complexity.get('probable_text_type', 'N/A')}")
        print(f"   Zone de focus:     {complexity.get('analysis_focus', 'N/A')}")
        print(f"   Qualité vocab.:    {complexity.get('vocabulary_assessment', 'N/A')}")
        
        analyzable = complexity.get('is_analyzable', False)
        print(f"   Analysable:        {'✅ Oui' if analyzable else '❌ Non'}")
        
        if not analyzable:
            print(f"   ⚠️  Attention: Texte trop court pour analyse fiable")
        
        print()
    
    # Effectuer l'analyse cryptographique
    results = analyzer.analyze_caesar(ciphertext, args.top)
    
    # Sortir les résultats
    if args.json:
        output_data = results
        
        if args.output:
            # Résoudre le chemin de sortie
            output_path = Path(args.output)
            if not output_path.is_absolute():
                output_path = PROJECT_ROOT / args.output
            analyzer.export_results(output_data, str(output_path))
            if not args.quiet:
                print(f"✅ Résultats sauvegardés dans {output_path}")
        else:
            print(json.dumps(output_data, indent=2, ensure_ascii=False))
    else:
        # Afficher joliment les résultats
        if not args.quiet:
            _print_pretty_results(results, args.verbose, args.top)
    
    # Détection de drapeau
    if args.find_flag:
        flag_found = analyzer.save_flag(results, args.flag_file)
        
        if not args.quiet:
            if flag_found:
                flag = analyzer.find_flag(results)
                print(f"\n🚩 DRAPEAU TROUVÉ: {flag}")
                print(f"✅ Sauvegardé dans: {args.flag_file}")
            else:
                print("\n⚠️  Aucun pattern FLAG{...} trouvé dans les meilleures solutions")
    
    # Afficher les statistiques intelligentes
    if not args.quiet and not args.json:
        stats = results.get('statistics', {})
        print(f"\n📊 STATISTIQUES INTELLIGENTES:")
        print(f"   Temps d'analyse:    {stats.get('analysis_time_seconds', 0):.3f}s")
        print(f"   Hypothèses testées: {stats.get('total_hypotheses', 0)}")
        print(f"   Plage des scores:   {stats.get('score_range', (0, 0))[0]:.1f} - {stats.get('score_range', (0, 0))[1]:.1f}")
        print(f"   Score moyen:        {stats.get('mean_score', 0):.1f}")
        print(f"   Écart-type:         {stats.get('std_deviation', 0):.1f}")
        print(f"   Écart de confiance: {stats.get('confidence_gap', 0):.1f}")
    
    if not args.quiet:
        print("\n" + "=" * 60)
        print("✅ Analyse intelligente terminée avec succès!")
    
    return 0


def _print_pretty_results(results: dict, verbose: bool = False, top_n: int = 5):
    """Affiche les résultats en format lisible pour humains."""
    best = results.get('best_solution')
    
    if best:
        print("\n🎯 MEILLEURE SOLUTION IDENTIFIÉE:")
        print(f"   Clé:          {best['key']}")
        print(f"   Score:        {best['score']}/100")
        print(f"   Confiance:    {best['confidence']}")
        print(f"\n📝 TEXTE DÉCHIFFRÉ:")
        print("-" * 40)
        print(best['plaintext'])
        if len(best['plaintext']) > 500:
            print("... [texte tronqué pour affichage]")
        print("-" * 40)
    
    # Tableau des meilleures solutions
    top_solutions = results.get('top_solutions', [])
    if top_solutions and (verbose or len(top_solutions) > 1):
        print(f"\n📋 TOP {len(top_solutions)} SOLUTIONS:")
        print("-" * 70)
        print(f"{'Rang':<4} {'Clé':<4} {'Score':<8} {'Confiance':<12} Aperçu")
        print("-" * 70)
        
        for i, sol in enumerate(top_solutions, 1):
            preview = sol['preview']
            if len(preview) > 40:
                preview = preview[:37] + "..."
            
            print(f"{i:<4} {sol['key']:<4} {sol['score']:<8.1f} {sol['confidence']:<12} {preview}")
        print("-" * 70)
    
    # Analyse fréquentielle si verbose
    if verbose:
        freq = results.get('frequency_analysis', {})
        if freq and 'most_common_letter' in freq:
            print(f"\n📈 ANALYSE FRÉQUENTIELLE:")
            print(f"   Lettre la plus commune: '{freq['most_common_letter']}'")
            print(f"   Clé estimée:           {freq['estimated_key']}")
            if 'top_frequencies' in freq:
                top_items = list(freq['top_frequencies'].items())[:3]
                top_str = ', '.join([f"'{k}'({v})" for k, v in top_items])
                print(f"   Top lettres:           {top_str}")


if __name__ == "__main__":
    # MODE DÉMO POUR THONNY - P1-C1 SPÉCIFIQUE
    import sys
    
    # Chemin vers le fichier de test - À ADAPTER À VOTRE SYSTÈME
    CHEMIN_PROJET = r"C:\Users\User\OneDrive\Bureau\p1-c1_crypto_analyzer"
    FICHIER_TEST = os.path.join(CHEMIN_PROJET, "test_message.txt")
    
    # Vérifier si exécution sans arguments (Thonny)
    if len(sys.argv) == 1:
        print("🚀 DÉMONSTRATION P1-C1 - CRYPTANALYSE INTELLIGENTE")
        print("=" * 60)
        print("Exécution avec analyse intelligente complète...")
        
        # Configurer les arguments de démonstration
        sys.argv = [
            'crack_caesar.py', 
            '--input', FICHIER_TEST,
            '--verbose',
            '--find-flag',
            '--complexity',
            '--top', '3'
        ]
    
    sys.exit(main())