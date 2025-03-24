"""
Module contenant la classe Food qui représente la nourriture dans le jeu.
"""

import pygame
import random
from enum import Enum
from src.utils.constants import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, RED, GREEN, BLUE, WHITE
)

class FoodType(Enum):
    """
    Énumération des types de nourriture.
    """
    NORMAL = 0  # Nourriture normale (pomme rouge)
    BONUS = 1   # Bonus (pomme dorée) - points supplémentaires
    SPEED = 2   # Bonus de vitesse (pomme bleue) - serpent plus rapide temporairement
    SLOW = 3    # Malus de vitesse (pomme verte) - serpent plus lent temporairement


class Food:
    """
    Classe représentant la nourriture (pomme) que le serpent peut manger.
    """
    
    def __init__(self, snake_body=None, level=1):
        """
        Initialise une nouvelle nourriture à une position aléatoire.
        
        Args:
            snake_body (list, optional): Liste des positions du corps du serpent pour éviter
                                        que la nourriture n'apparaisse sur le serpent.
            level (int, optional): Niveau actuel pour déterminer les types de nourriture disponibles.
        """
        self.level = level
        self.position = self._generate_random_position(snake_body)
        self.type = self._get_random_type()
        self.creation_time = pygame.time.get_ticks()
        self.active_time = 10000  # Temps pendant lequel la nourriture reste active (10 sec)
        
        # Points attribués pour chaque type de nourriture
        self.points = {
            FoodType.NORMAL: 10,
            FoodType.BONUS: 30,
            FoodType.SPEED: 20,
            FoodType.SLOW: 5
        }
    
    def _get_random_type(self):
        """
        Détermine un type de nourriture aléatoire en fonction du niveau.
        
        Returns:
            FoodType: Type de nourriture
        """
        # Niveau 1: seulement de la nourriture normale
        if self.level < 2:
            return FoodType.NORMAL
        
        # Niveau 2+: possibilité de différents types de nourriture
        choices = [FoodType.NORMAL] * 70  # 70% de nourriture normale
        
        if self.level >= 2:
            choices.extend([FoodType.BONUS] * 20)  # 20% de bonus
        
        if self.level >= 3:
            choices.extend([FoodType.SPEED] * 5)  # 5% de bonus de vitesse
            choices.extend([FoodType.SLOW] * 5)   # 5% de malus de vitesse
        
        return random.choice(choices)
    
    def _generate_random_position(self, snake_body=None, obstacles=None):
        """
        Génère une position aléatoire pour la nourriture qui n'est pas sur le serpent ou les obstacles.
        
        Args:
            snake_body (list, optional): Liste des positions du corps du serpent.
            obstacles (list, optional): Liste des obstacles.
            
        Returns:
            tuple: (x, y) coordonnées de la nouvelle position
        """
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            # Vérifier que la position n'est pas sur le serpent
            if snake_body is not None and (x, y) in snake_body:
                continue
            
            # Vérifier que la position n'est pas sur un obstacle
            if obstacles is not None:
                if any(obs.position == (x, y) for obs in obstacles):
                    continue
            
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
    
    def should_expire(self):
        """
        Vérifie si la nourriture devrait expirer (seulement pour les types spéciaux).
        
        Returns:
            bool: True si la nourriture doit être remplacée, False sinon
        """
        if self.type == FoodType.NORMAL:
            return False
        
        current_time = pygame.time.get_ticks()
        return current_time - self.creation_time > self.active_time
    
    def get_points(self):
        """
        Retourne le nombre de points attribués pour ce type de nourriture.
        
        Returns:
            int: Nombre de points
        """
        return self.points[self.type]
    
    def respawn(self, snake_body, obstacles=None, level=None):
        """
        Déplace la nourriture à une nouvelle position aléatoire.
        
        Args:
            snake_body (list): Liste des positions du corps du serpent
            obstacles (list, optional): Liste des obstacles.
            level (int, optional): Niveau actuel pour déterminer les types de nourriture disponibles.
        """
        if level is not None:
            self.level = level
        
        self.position = self._generate_random_position(snake_body, obstacles)
        self.type = self._get_random_type()
        self.creation_time = pygame.time.get_ticks()
    
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
        
        # Couleur selon le type
        if self.type == FoodType.NORMAL:
            color = RED
        elif self.type == FoodType.BONUS:
            color = (255, 215, 0)  # Or
        elif self.type == FoodType.SPEED:
            color = BLUE
        elif self.type == FoodType.SLOW:
            color = GREEN
        
        pygame.draw.circle(screen, color, center, radius)
        
        # Pour les types spéciaux, ajouter un effet visuel (pulsation ou brillance)
        if self.type != FoodType.NORMAL:
            # Effet de pulsation basé sur le temps
            current_time = pygame.time.get_ticks()
            pulse = abs(((current_time - self.creation_time) % 1000) - 500) / 500  # Valeur entre 0 et 1
            
            # Dessiner un cercle intérieur
            inner_radius = int(radius * (0.5 + pulse * 0.2))
            pygame.draw.circle(screen, WHITE, center, inner_radius)
