"""
Module contenant la classe Snake qui représente le serpent dans le jeu.
"""

import pygame
from enum import Enum
from collections import deque
from src.utils.constants import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, GREEN, DARK_GREEN
)

class Direction(Enum):
    """
    Énumération des directions possibles pour le serpent.
    """
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Snake:
    """
    Classe représentant le serpent contrôlé par le joueur.
    """
    
    def __init__(self):
        """
        Initialise un nouveau serpent au centre de l'écran.
        """
        # Position initiale au centre de l'écran
        self.x = GRID_WIDTH // 2
        self.y = GRID_HEIGHT // 2
        
        # Corps du serpent (liste de segments)
        self.body = deque([(self.x, self.y), (self.x - 1, self.y), (self.x - 2, self.y)])
        
        # Direction initiale (vers la droite)
        self.direction = Direction.RIGHT
        
        # Indicateur pour savoir si le serpent vient de manger
        self.just_ate = False
        
        # État du serpent
        self.alive = True
    
    def change_direction(self, new_direction):
        """
        Change la direction du serpent si ce n'est pas un demi-tour.
        
        Args:
            new_direction (Direction): La nouvelle direction souhaitée
        """
        # Empêcher le serpent de faire demi-tour
        if (self.direction == Direction.UP and new_direction == Direction.DOWN) or \
           (self.direction == Direction.DOWN and new_direction == Direction.UP) or \
           (self.direction == Direction.LEFT and new_direction == Direction.RIGHT) or \
           (self.direction == Direction.RIGHT and new_direction == Direction.LEFT):
            return
        
        self.direction = new_direction
    
    def get_next_head_position(self):
        """
        Calcule la prochaine position de la tête du serpent sans le déplacer.
        
        Returns:
            tuple: (x, y) coordonnées de la prochaine position de la tête
        """
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        return (head_x + dx, head_y + dy)
    
    def move(self):
        """
        Déplace le serpent dans sa direction actuelle.
        
        Returns:
            bool: True si le serpent est toujours vivant, False sinon
        """
        if not self.alive:
            return False
        
        # Calculer la nouvelle position de la tête
        dx, dy = self.direction.value
        new_head = (self.body[0][0] + dx, self.body[0][1] + dy)
        
        # Vérifier si le serpent se mord lui-même
        if new_head in list(self.body)[1:]:
            self.alive = False
            return False
        
        # Vérifier les collisions avec les murs
        x, y = new_head
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            self.alive = False
            return False
        
        # Ajouter la nouvelle tête
        self.body.appendleft(new_head)
        
        # Supprimer la queue si le serpent n'a pas mangé
        if not self.just_ate:
            self.body.pop()
        else:
            self.just_ate = False
        
        return True
    
    def grow(self):
        """
        Fait grandir le serpent (appelé lorsqu'il mange).
        """
        self.just_ate = True
    
    def get_head_position(self):
        """
        Renvoie la position actuelle de la tête du serpent.
        
        Returns:
            tuple: (x, y) coordonnées de la tête
        """
        return self.body[0]
    
    def draw(self, screen):
        """
        Dessine le serpent sur l'écran.
        
        Args:
            screen (pygame.Surface): Surface de l'écran
        """
        # Dessiner chaque segment du corps
        for i, (x, y) in enumerate(self.body):
            # Tête en vert foncé, corps en vert
            color = DARK_GREEN if i == 0 else GREEN
            
            # Dessiner un rectangle pour chaque segment
            rect = pygame.Rect(
                x * GRID_SIZE, 
                y * GRID_SIZE, 
                GRID_SIZE, 
                GRID_SIZE
            )
            pygame.draw.rect(screen, color, rect)
            
            # Dessiner un contour plus clair
            pygame.draw.rect(screen, DARK_GREEN, rect, 1)
