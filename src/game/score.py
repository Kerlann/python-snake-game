"""
Module contenant la classe Score qui gère le score du joueur.
"""

import pygame
from src.utils.constants import WHITE

class Score:
    """
    Classe gérant le score du joueur et son affichage.
    """
    
    def __init__(self):
        """
        Initialise un nouveau score à zéro.
        """
        self.value = 0
        self.font = pygame.font.Font(None, 36)
    
    def increase(self, points=10):
        """
        Augmente le score du joueur.
        
        Args:
            points (int, optional): Nombre de points à ajouter. Par défaut 10.
        """
        self.value += points
    
    def reset(self):
        """
        Réinitialise le score à zéro.
        """
        self.value = 0
    
    def draw(self, screen, x=10, y=10):
        """
        Affiche le score à l'écran.
        
        Args:
            screen (pygame.Surface): Surface de l'écran
            x (int, optional): Coordonnée X. Par défaut 10.
            y (int, optional): Coordonnée Y. Par défaut 10.
        """
        score_text = self.font.render(f"Score: {self.value}", True, WHITE)
        screen.blit(score_text, (x, y))
