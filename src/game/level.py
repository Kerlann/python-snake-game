"""
Module contenant la classe Level qui gère les niveaux et la difficulté du jeu.
"""

import pygame
import random
from src.utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT
)

class Obstacle:
    """
    Classe représentant un obstacle dans le jeu.
    """
    def __init__(self, position):
        """
        Initialise un nouvel obstacle.
        
        Args:
            position (tuple): Position (x, y) de l'obstacle sur la grille
        """
        self.position = position
        self.color = (100, 100, 100)  # Gris
    
    def draw(self, screen):
        """
        Dessine l'obstacle sur l'écran.
        
        Args:
            screen (pygame.Surface): Surface de l'écran
        """
        x, y = self.position
        rect = pygame.Rect(
            x * GRID_SIZE, 
            y * GRID_SIZE, 
            GRID_SIZE, 
            GRID_SIZE
        )
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (50, 50, 50), rect, 1)  # Bordure


class Level:
    """
    Classe gérant les niveaux et la difficulté du jeu.
    """
    
    def __init__(self):
        """
        Initialise un nouveau gestionnaire de niveaux.
        """
        self.current_level = 1
        self.score_for_next_level = 100  # Score nécessaire pour passer au niveau suivant
        self.level_multiplier = 1.5  # Multiplicateur pour le score du niveau suivant
        
        self.base_speed = 10  # Vitesse de base du serpent
        self.current_speed = self.base_speed
        
        self.obstacles = []
        self.font = pygame.font.Font(None, 24)
        
        # Nombre d'obstacles par niveau
        self.obstacles_per_level = 3
    
    def get_current_speed(self):
        """
        Retourne la vitesse actuelle du serpent en fonction du niveau.
        
        Returns:
            float: Vitesse actuelle
        """
        return self.current_speed
    
    def check_level_up(self, score):
        """
        Vérifie si le joueur doit passer au niveau suivant.
        
        Args:
            score (int): Score actuel du joueur
            
        Returns:
            bool: True si le niveau a changé, False sinon
        """
        if score >= self.score_for_next_level:
            self.level_up()
            return True
        return False
    
    def level_up(self):
        """
        Passe au niveau suivant et augmente la difficulté.
        """
        self.current_level += 1
        
        # Augmenter le score nécessaire pour le prochain niveau
        self.score_for_next_level = int(self.score_for_next_level * self.level_multiplier)
        
        # Augmenter la vitesse du serpent
        self.current_speed = self.base_speed + (self.current_level - 1) * 2
        
        # Ajouter des obstacles (seulement pour les niveaux > 2)
        if self.current_level > 2:
            self.generate_obstacles()
    
    def generate_obstacles(self):
        """
        Génère des obstacles aléatoires pour le niveau actuel.
        """
        # Limiter le nombre d'obstacles
        max_obstacles = self.obstacles_per_level * (self.current_level - 2)
        
        # Ajouter de nouveaux obstacles
        for _ in range(self.obstacles_per_level):
            # Générer une position aléatoire, pas trop près des bords
            x = random.randint(2, GRID_WIDTH - 3)
            y = random.randint(2, GRID_HEIGHT - 3)
            
            # Éviter de placer un obstacle sur un autre
            if not any(obs.position == (x, y) for obs in self.obstacles):
                self.obstacles.append(Obstacle((x, y)))
    
    def check_obstacle_collision(self, position):
        """
        Vérifie si une position est en collision avec un obstacle.
        
        Args:
            position (tuple): Position (x, y) à vérifier
            
        Returns:
            bool: True s'il y a une collision, False sinon
        """
        return any(obs.position == position for obs in self.obstacles)
    
    def draw(self, screen):
        """
        Dessine les obstacles et le niveau actuel sur l'écran.
        
        Args:
            screen (pygame.Surface): Surface de l'écran
        """
        # Dessiner les obstacles
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        
        # Afficher le niveau actuel
        level_text = self.font.render(f"Niveau: {self.current_level}", True, WHITE)
        screen.blit(level_text, (WINDOW_WIDTH - 120, 10))
