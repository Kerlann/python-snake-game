"""
Tests unitaires pour la classe Score.
"""

import unittest
import sys
import os
import pygame

# Ajouter le répertoire parent au chemin de recherche pour importer le module src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game.score import Score

# Initialisation de Pygame pour les tests
pygame.init()

class TestScore(unittest.TestCase):
    """
    Tests pour la classe Score.
    """
    
    def setUp(self):
        """
        Initialisation avant chaque test.
        """
        self.score = Score()
    
    def test_init(self):
        """
        Test de l'initialisation d'un score.
        """
        # Vérifier que le score initial est 0
        self.assertEqual(self.score.value, 0)
        
        # Vérifier que la police est initialisée
        self.assertIsNotNone(self.score.font)
    
    def test_increase(self):
        """
        Test de la méthode increase.
        """
        # Valeur initiale
        initial_value = self.score.value
        
        # Augmenter le score avec la valeur par défaut (10)
        self.score.increase()
        self.assertEqual(self.score.value, initial_value + 10)
        
        # Augmenter le score avec une valeur spécifique
        self.score.increase(25)
        self.assertEqual(self.score.value, initial_value + 10 + 25)
    
    def test_reset(self):
        """
        Test de la méthode reset.
        """
        # Augmenter le score
        self.score.increase(50)
        self.assertEqual(self.score.value, 50)
        
        # Réinitialiser le score
        self.score.reset()
        self.assertEqual(self.score.value, 0)
    
    def test_draw(self):
        """
        Test de la méthode draw (vérification basique).
        """
        # Créer une surface pour le test
        screen = pygame.Surface((800, 600))
        
        # Vérifier que draw() ne génère pas d'exception
        try:
            self.score.draw(screen)
            success = True
        except Exception as e:
            success = False
            self.fail(f"draw() a généré une exception: {e}")
        
        self.assertTrue(success)
        
        # Vérifier que l'affichage change lorsque le score change
        # (Test indirecte car nous ne pouvons pas facilement vérifier le rendu graphique)
        initial_render = self.score.font.render(f"Score: {self.score.value}", True, (255, 255, 255))
        
        # Augmenter le score et vérifier que le rendu change
        self.score.increase(100)
        new_render = self.score.font.render(f"Score: {self.score.value}", True, (255, 255, 255))
        
        # Les rendus devraient être différents (taille différente)
        self.assertNotEqual(initial_render.get_width(), new_render.get_width())

if __name__ == '__main__':
    unittest.main()
