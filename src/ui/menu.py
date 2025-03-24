"""
Module contenant les classes liées au menu principal du jeu.
"""

import pygame
from enum import Enum
from src.utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE,
    GREEN, DARK_GREEN, GAME_TITLE
)

class MenuOption(Enum):
    """
    Énumération des options possibles du menu.
    """
    PLAY = 0
    OPTIONS = 1
    QUIT = 2


class Menu:
    """
    Classe représentant le menu principal du jeu.
    """
    
    def __init__(self):
        """
        Initialise un nouveau menu.
        """
        self.options = ["Jouer", "Options", "Quitter"]
        self.selected_option = 0
        
        # Polices
        self.title_font = pygame.font.Font(None, 72)
        self.option_font = pygame.font.Font(None, 48)
        
        # Couleurs
        self.title_color = GREEN
        self.option_color = WHITE
        self.selected_color = DARK_GREEN
        
        # Timing pour animation
        self.animation_timer = 0
        
        # État
        self.return_value = None
    
    def process_events(self, events):
        """
        Gère les événements du menu.
        
        Args:
            events (list): Liste des événements Pygame
            
        Returns:
            MenuOption or None: L'option sélectionnée ou None
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return MenuOption(self.selected_option)
        
        return None
    
    def update(self, dt):
        """
        Met à jour l'état du menu.
        
        Args:
            dt (float): Temps écoulé depuis la dernière mise à jour
        """
        # Animation du titre ou autres effets
        self.animation_timer += dt
    
    def draw(self, screen):
        """
        Dessine le menu sur l'écran.
        
        Args:
            screen (pygame.Surface): Surface de l'écran
        """
        # Effacer l'écran
        screen.fill(BLACK)
        
        # Dessiner le titre
        title_text = self.title_font.render(GAME_TITLE, True, self.title_color)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
        screen.blit(title_text, title_rect)
        
        # Dessiner les options
        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected_option else self.option_color
            option_text = self.option_font.render(option, True, color)
            option_rect = option_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 60)
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
