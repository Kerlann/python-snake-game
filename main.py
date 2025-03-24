#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Jeu Snake en Python avec Pygame
Point d'entrée principal du programme
"""

import argparse
from src.game.game import Game

def main():
    """
    Fonction principale qui initialise et lance le jeu.
    """
    # Parser les arguments de ligne de commande
    parser = argparse.ArgumentParser(description='Jeu Snake en Python avec Pygame')
    parser.add_argument('--debug', action='store_true', help='Activer le mode débogage')
    parser.add_argument('--test', action='store_true', help='Exécuter les tests')
    args = parser.parse_args()
    
    # Exécuter les tests si demandé
    if args.test:
        print("Exécution des tests...")
        import unittest
        import os
        import sys
        
        # Ajouter le répertoire des tests au chemin de recherche
        tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
        sys.path.insert(0, tests_dir)
        
        # Importer et exécuter les tests
        from tests.run_tests import run_tests
        return run_tests()
    
    # Sinon, lancer le jeu
    print("Initialisation du jeu Snake...")
    game = Game(debug_mode=args.debug)
    game.run()

if __name__ == "__main__":
    main()
