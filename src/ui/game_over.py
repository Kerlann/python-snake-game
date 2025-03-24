"""
Module contenant les classes liées à l'écran de Game Over.
"""

import pygame
from enum import Enum
from src.utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE,
    GREEN, RED
)

class GameOverOption(Enum):
    """
    Énumération des options possibles de l'écran Game Over.
    """
    PLAY_AGAIN = 0
    MENU = 1
    QUIT = 2


class GameOverScreen:
    """
    Classe représentant l'écran de Game Over.
    """
    
    def __init__(self, score):
        """
        Initialise un nouvel écran de Game Over.
        
        Args:
            score (int): Le score final du joueur
        """
        self.score = score
        self.options = ["Rejouer", "Menu Principal", "Quitter"]
        self.selected_option = 0
        
        # Polices
        self.title_font = pygame.font.Font(None, 72)
        self.score_font = pygame.font.Font(None, 54)
        self.option_font = pygame.font.Font(None, 48)
        
        # Couleurs
        self.title_color = RED
        self.score_color = WHITE
        self.option_color = WHITE
        self.selected_color = GREEN
    
    def process_events(self, events):
        """
        Gère les événements de l'écran de Game Over.
        
        Args:
            events (list): Liste des événements Pygame
            
        Returns:
            GameOverOption or None: L'option sélectionnée ou None
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return GameOverOption(self.selected_option)
        
        return None
    
    def update(self, dt):
        """
        Met à jour l'état de l'écran de Game Over.
        
        Args:
            dt (float): Temps écoulé depuis la dernière mise à jour
        """
        # Animation ou autres effets
        pass
    
    def draw(self, screen):
        """
        Dessine l'écran de Game Over sur l'écran.
        
        Args:
            screen (pygame.Surface): Surface de l'écran
        """
        # Effacer l'écran
        screen.fill(BLACK)
        
        # Dessiner le titre
        title_text = self.title_font.render("GAME OVER", True, self.title_color)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
        screen.blit(title_text, title_rect)
        
        # Dessiner le score
        score_text = self.score_font.render(f"Score: {self.score}", True, self.score_color)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 20))
        screen.blit(score_text, score_rect)
        
        # Dessiner les options
        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected_option else self.option_color
            option_text = self.option_font.render(option, True, color)
            option_rect = option_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50 + i * 60)
            )
            screen.blit(option_text, option_rect)
            
            # Indicateur de sélection (flèche)
            if i == self.selected_option:
                arrow_text = self.option_font.render(">", True, self.selected_color)
                arrow_rect = arrow_text.get_rect(
                    right=option_rect.left - 10,
                    centery=option_rect.centery
                )
                screen.blit(arrow_text, arrow_rect)
