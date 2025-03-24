"""
Module contenant la classe Food qui représente la nourriture dans le jeu.
"""

import pygame
import random
from src.utils.constants import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, RED
)

class Food:
    """
    Classe représentant la nourriture (pomme) que le serpent peut manger.
    """
    
    def __init__(self, snake_body=None):
        """
        Initialise une nouvelle nourriture à une position aléatoire.
        
        Args:
            snake_body (list, optional): Liste des positions du corps du serpent pour éviter
                                        que la nourriture n'apparaisse sur le serpent.
        """
        self.position = self._generate_random_position(snake_body)
    
    def _generate_random_position(self, snake_body=None):
        """
        Génère une position aléatoire pour la nourriture qui n'est pas sur le serpent.
        
        Args:
            snake_body (list, optional): Liste des positions du corps du serpent.
            
        Returns:
            tuple: (x, y) coordonnées de la nouvelle position
        """
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            # Si le serpent n'est pas fourni ou si la position n'est pas sur le serpent
            if snake_body is None or (x, y) not in snake_body:
                return (x, y)
    
    def is_collision(self, position):
        """
        Vérifie si une position (comme la tête du serpent) est en collision avec la nourriture.
        
        Args:
            position (tuple): Position (x, y) à vérifier
            
        Returns:
            bool: True s'il y a une collision, False sinon
        """
        return self.position == position
    
    def respawn(self, snake_body):
        """
        Déplace la nourriture à une nouvelle position aléatoire.
        
        Args:
            snake_body (list): Liste des positions du corps du serpent
        """
        self.position = self._generate_random_position(snake_body)
    
    def draw(self, screen):
        """
        Dessine la nourriture sur l'écran.
        
        Args:
            screen (pygame.Surface): Surface de l'écran
        """
        x, y = self.position
        
        # Dessiner un cercle pour la nourriture
        rect = pygame.Rect(
            x * GRID_SIZE, 
            y * GRID_SIZE, 
            GRID_SIZE, 
            GRID_SIZE
        )
        
        # Centre et rayon du cercle
        center = rect.center
        radius = GRID_SIZE // 2 - 2
        
        pygame.draw.circle(screen, RED, center, radius)
