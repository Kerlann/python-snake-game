"""
Script pour exécuter tous les tests du projet.
"""

import unittest
import sys
import os

# Ajouter le répertoire parent au chemin de recherche pour importer le module src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_tests():
    """
    Découvre et exécute tous les tests.
    
    Returns:
        int: 0 si tous les tests passent, 1 sinon
    """
    # Découvrir et exécuter tous les tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(os.path.dirname(__file__), pattern='test_*.py')
    
    # Exécuter les tests et afficher les résultats
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    
    # Retourner le code approprié (0 si tous les tests passent, 1 sinon)
    return int(not result.wasSuccessful())

if __name__ == '__main__':
    sys.exit(run_tests())
