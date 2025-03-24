"""
Tests unitaires pour la classe Food.
"""

import unittest
import sys
import os
import pygame

# Ajouter le répertoire parent au chemin de recherche pour importer le module src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game.food import Food, FoodType
from src.utils.constants import GRID_WIDTH, GRID_HEIGHT

# Initialisation de Pygame pour les tests
pygame.init()

class TestFood(unittest.TestCase):
    """
    Tests pour la classe Food.
    """
    
    def setUp(self):
        """
        Initialisation avant chaque test.
        """
        # Créer un serpent simulé (une liste de positions)
        self.snake_body = [(5, 5), (4, 5), (3, 5)]
        
        # Créer une nourriture
        self.food = Food(self.snake_body, level=1)
    
    def test_init(self):
        """
        Test de l'initialisation d'une nourriture.
        """
        # Vérifier que la position est valide
        x, y = self.food.position
        self.assertTrue(0 <= x < GRID_WIDTH)
        self.assertTrue(0 <= y < GRID_HEIGHT)
        
        # Vérifier que la nourriture n'est pas sur le serpent
        self.assertNotIn(self.food.position, self.snake_body)
        
        # Vérifier le type (niveau 1 = type normal)
        self.assertEqual(self.food.type, FoodType.NORMAL)
    
    def test_respawn(self):
        """
        Test de la méthode respawn.
        """
        # Position initiale
        initial_position = self.food.position
        
        # Faire réapparaître la nourriture
        self.food.respawn(self.snake_body)
        
        # Vérifier que la position a changé
        self.assertNotEqual(self.food.position, initial_position)
        
        # Vérifier que la nouvelle position est valide
        x, y = self.food.position
        self.assertTrue(0 <= x < GRID_WIDTH)
        self.assertTrue(0 <= y < GRID_HEIGHT)
        
        # Vérifier que la nourriture n'est pas sur le serpent
        self.assertNotIn(self.food.position, self.snake_body)
    
    def test_is_collision(self):
        """
        Test de la méthode is_collision.
        """
        # Position de la nourriture
        food_pos = self.food.position
        
        # Vérifier une collision
        self.assertTrue(self.food.is_collision(food_pos))
        
        # Vérifier une non-collision
        non_food_pos = (food_pos[0] + 1, food_pos[1])
        self.assertFalse(self.food.is_collision(non_food_pos))
    
    def test_food_types(self):
        """
        Test des différents types de nourriture.
        """
        # Niveau 1 devrait toujours donner une nourriture normale
        level1_food = Food(self.snake_body, level=1)
        self.assertEqual(level1_food.type, FoodType.NORMAL)
        
        # Niveau 2+ peut donner différents types
        # Note: comme les types sont aléatoires, on ne peut pas tester directement
        # Mais on peut vérifier que les points sont corrects pour chaque type
        
        # Points pour la nourriture normale
        self.assertEqual(self.food.points[FoodType.NORMAL], 10)
        
        # Points pour la nourriture bonus
        self.assertEqual(self.food.points[FoodType.BONUS], 30)
        
        # Points pour la nourriture vitesse
        self.assertEqual(self.food.points[FoodType.SPEED], 20)
        
        # Points pour la nourriture ralentissement
        self.assertEqual(self.food.points[FoodType.SLOW], 5)
    
    def test_get_points(self):
        """
        Test de la méthode get_points.
        """
        # Définir manuellement le type de nourriture
        self.food.type = FoodType.NORMAL
        self.assertEqual(self.food.get_points(), 10)
        
        self.food.type = FoodType.BONUS
        self.assertEqual(self.food.get_points(), 30)
        
        self.food.type = FoodType.SPEED
        self.assertEqual(self.food.get_points(), 20)
        
        self.food.type = FoodType.SLOW
        self.assertEqual(self.food.get_points(), 5)
    
    def test_should_expire(self):
        """
        Test de la méthode should_expire.
        """
        # La nourriture normale ne devrait jamais expirer
        self.food.type = FoodType.NORMAL
        self.assertFalse(self.food.should_expire())
        
        # Les autres types devraient expirer après un certain temps
        self.food.type = FoodType.BONUS
        self.food.creation_time = pygame.time.get_ticks() - self.food.active_time - 1
        self.assertTrue(self.food.should_expire())

if __name__ == '__main__':
    unittest.main()
