"""
Module contenant la classe HighScoreScreen qui affiche l'écran des meilleurs scores.
"""

import pygame
from enum import Enum
from src.utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, GREEN, RED
)

class HighScoreScreenOption(Enum):
    """
    Énumération des options possibles de l'écran des meilleurs scores.
    """
    BACK = 0
    RESET = 1


class HighScoreScreen:
    """
    Classe représentant l'écran d'affichage des meilleurs scores.
    """
    
    def __init__(self, highscore_manager):
        """
        Initialise un nouvel écran de meilleurs scores.
        
        Args:
            highscore_manager (HighScore): Gestionnaire de meilleurs scores
        """
        self.highscore_manager = highscore_manager
        self.options = ["Retour", "Réinitialiser les scores"]
        self.selected_option = 0
        
        # Polices
        self.title_font = pygame.font.Font(None, 48)
        self.option_font = pygame.font.Font(None, 36)
        
        # Couleurs
        self.title_color = GREEN
        self.option_color = WHITE
        self.selected_color = GREEN
        self.reset_color = RED
    
    def process_events(self, events):
        """
        Gère les événements de l'écran des meilleurs scores.
        
        Args:
            events (list): Liste des événements Pygame
            
        Returns:
            HighScoreScreenOption or None: L'option sélectionnée ou None
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return HighScoreScreenOption.BACK
                elif event.key == pygame.K_LEFT:
                    self.selected_option = 0  # Sélectionner "Retour"
                elif event.key == pygame.K_RIGHT:
                    self.selected_option = 1  # Sélectionner "Réinitialiser"
                elif event.key == pygame.K_RETURN:
                    return HighScoreScreenOption(self.selected_option)
        
        return None
    
    def draw(self, screen):
        """
        Dessine l'écran des meilleurs scores.
        
        Args:
            screen (pygame.Surface): Surface de l'écran
        """
        # Dessiner les meilleurs scores (utilise la méthode du gestionnaire)
        self.highscore_manager.draw_high_scores(screen)
        
        # Dessiner les options en bas de l'écran
        button_y = WINDOW_HEIGHT - 80
        
        # Option "Retour"
        back_color = self.selected_color if self.selected_option == 0 else self.option_color
        back_text = self.option_font.render("Retour", True, back_color)
        back_rect = back_text.get_rect(center=(WINDOW_WIDTH // 3, button_y))
        screen.blit(back_text, back_rect)
        
        # Option "Réinitialiser"
        reset_color = self.reset_color if self.selected_option == 1 else self.option_color
        reset_text = self.option_font.render("Réinitialiser", True, reset_color)
        reset_rect = reset_text.get_rect(center=(WINDOW_WIDTH * 2 // 3, button_y))
        screen.blit(reset_text, reset_rect)
        
        # Indicateur de sélection
        if self.selected_option == 0:
            # Souligner "Retour"
            pygame.draw.line(
                screen, 
                back_color, 
                (back_rect.left, back_rect.bottom + 2), 
                (back_rect.right, back_rect.bottom + 2), 
                2
            )
        else:
            # Souligner "Réinitialiser"
            pygame.draw.line(
                screen, 
                reset_color, 
                (reset_rect.left, reset_rect.bottom + 2), 
                (reset_rect.right, reset_rect.bottom + 2), 
                2
            )
