"""
Tests unitaires pour la classe Snake.
"""

import unittest
import sys
import os

# Ajouter le répertoire parent au chemin de recherche pour importer le module src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game.snake import Snake, Direction

class TestSnake(unittest.TestCase):
    """
    Tests pour la classe Snake.
    """
    
    def setUp(self):
        """
        Initialisation avant chaque test.
        """
        self.snake = Snake()
    
    def test_init(self):
        """
        Test de l'initialisation d'un serpent.
        """
        # Vérifier la direction initiale
        self.assertEqual(self.snake.direction, Direction.RIGHT)
        
        # Vérifier que le serpent est vivant
        self.assertTrue(self.snake.alive)
        
        # Vérifier la longueur initiale du serpent (3 segments)
        self.assertEqual(len(self.snake.body), 3)
        
        # Vérifier que le serpent n'a pas mangé
        self.assertFalse(self.snake.just_ate)
    
    def test_get_head_position(self):
        """
        Test de la méthode get_head_position.
        """
        head_pos = self.snake.get_head_position()
        self.assertEqual(head_pos, self.snake.body[0])
    
    def test_change_direction(self):
        """
        Test de la méthode change_direction.
        """
        # Direction initiale: droite
        self.assertEqual(self.snake.direction, Direction.RIGHT)
        
        # Changer la direction vers le haut
        self.snake.change_direction(Direction.UP)
        self.assertEqual(self.snake.direction, Direction.UP)
        
        # Tenter de faire demi-tour (bas) - ne devrait pas changer
        self.snake.change_direction(Direction.DOWN)
        self.assertEqual(self.snake.direction, Direction.UP)
        
        # Changer la direction vers la gauche
        self.snake.change_direction(Direction.LEFT)
        self.assertEqual(self.snake.direction, Direction.LEFT)
        
        # Tenter de faire demi-tour (droite) - ne devrait pas changer
        self.snake.change_direction(Direction.RIGHT)
        self.assertEqual(self.snake.direction, Direction.LEFT)
    
    def test_move(self):
        """
        Test de la méthode move.
        """
        # Position initiale de la tête
        initial_head = self.snake.get_head_position()
        
        # Déplacer le serpent vers la droite
        self.snake.move()
        
        # Nouvelle position de la tête
        new_head = self.snake.get_head_position()
        
        # La tête devrait se déplacer d'une case vers la droite
        self.assertEqual(new_head[0], initial_head[0] + 1)
        self.assertEqual(new_head[1], initial_head[1])
        
        # La longueur du serpent devrait rester la même
        self.assertEqual(len(self.snake.body), 3)
    
    def test_grow(self):
        """
        Test de la méthode grow.
        """
        # Longueur initiale
        initial_length = len(self.snake.body)
        
        # Faire grandir le serpent
        self.snake.grow()
        
        # Déplacer le serpent pour appliquer la croissance
        self.snake.move()
        
        # La longueur devrait augmenter de 1
        self.assertEqual(len(self.snake.body), initial_length + 1)
    
    def test_collision_with_self(self):
        """
        Test de collision du serpent avec lui-même.
        """
        # Créer une situation où le serpent se mord la queue
        # Direction initiale: droite
        self.snake.change_direction(Direction.UP)
        self.snake.move()
        self.snake.change_direction(Direction.LEFT)
        self.snake.move()
        self.snake.change_direction(Direction.DOWN)
        self.snake.move()
        
        # La tête va entrer en collision avec le corps
        result = self.snake.move()
        
        # Le serpent devrait être mort
        self.assertFalse(result)
        self.assertFalse(self.snake.alive)
    
    def test_collision_with_wall(self):
        """
        Test de collision du serpent avec un mur.
        """
        # Forcer le serpent à sortir des limites
        # Créer un serpent près du bord
        from src.utils.constants import GRID_WIDTH
        self.snake = Snake()
        
        # Positionner le serpent tout à droite
        self.snake.body.clear()
        x = GRID_WIDTH - 1
        y = 5
        self.snake.body.extend([(x, y), (x-1, y), (x-2, y)])
        
        # Déplacer le serpent vers la droite (hors des limites)
        result = self.snake.move()
        
        # Le serpent devrait être mort
        self.assertFalse(result)
        self.assertFalse(self.snake.alive)

if __name__ == '__main__':
    unittest.main()
