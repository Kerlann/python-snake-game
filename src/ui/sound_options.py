"""
Module contenant les classes liées aux options sonores du jeu.
"""

import pygame
from enum import Enum
from src.utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, GREEN, RED
)
from src.utils.sound_manager import SoundEffect

class SoundOptionAction(Enum):
    """
    Énumération des actions possibles dans les options sonores.
    """
    BACK = 0
    TOGGLE_SOUND = 1
    TOGGLE_MUSIC = 2
    SOUND_VOLUME_UP = 3
    SOUND_VOLUME_DOWN = 4
    MUSIC_VOLUME_UP = 5
    MUSIC_VOLUME_DOWN = 6


class SoundOptions:
    """
    Classe représentant l'écran des options sonores.
    """
    
    def __init__(self, sound_manager):
        """
        Initialise un nouvel écran d'options sonores.
        
        Args:
            sound_manager (SoundManager): Gestionnaire de sons
        """
        self.sound_manager = sound_manager
        
        # Polices
        self.title_font = pygame.font.Font(None, 48)
        self.option_font = pygame.font.Font(None, 36)
        
        # Couleurs
        self.title_color = GREEN
        self.option_color = WHITE
        self.selected_color = GREEN
        self.disabled_color = RED
        
        # Options et sélection
        self.selected_option = 0
        self.options = [
            "Retour",
            "Sons: " + ("Activés" if sound_manager.sound_enabled else "Désactivés"),
            "Musique: " + ("Activée" if sound_manager.music_enabled else "Désactivée"),
            "Volume des sons: ",
            "Volume de la musique: "
        ]
        
        # Rectangle pour les barres de volume
        self.sound_volume_rect = pygame.Rect(
            WINDOW_WIDTH // 2 + 50, 
            WINDOW_HEIGHT // 2, 
            200, 
            20
        )
        self.music_volume_rect = pygame.Rect(
            WINDOW_WIDTH // 2 + 50, 
            WINDOW_HEIGHT // 2 + 50, 
            200, 
            20
        )
    
    def _update_options_text(self):
        """
        Met à jour le texte des options en fonction de l'état du gestionnaire de sons.
        """
        self.options[1] = "Sons: " + ("Activés" if self.sound_manager.sound_enabled else "Désactivés")
        self.options[2] = "Musique: " + ("Activée" if self.sound_manager.music_enabled else "Désactivée")
    
    def process_events(self, events):
        """
        Gère les événements de l'écran des options sonores.
        
        Args:
            events (list): Liste des événements Pygame
            
        Returns:
            SoundOptionAction or None: L'action sélectionnée ou None
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return SoundOptionAction.BACK
                
                # Navigation
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                    self.sound_manager.play_sound(SoundEffect.MENU_NAVIGATE)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                    self.sound_manager.play_sound(SoundEffect.MENU_NAVIGATE)
                
                # Action sur l'option sélectionnée
                elif event.key == pygame.K_RETURN:
                    self.sound_manager.play_sound(SoundEffect.MENU_SELECT)
                    
                    if self.selected_option == 0:  # Retour
                        return SoundOptionAction.BACK
                    elif self.selected_option == 1:  # Toggle son
                        self.sound_manager.toggle_sound()
                        self._update_options_text()
                        return SoundOptionAction.TOGGLE_SOUND
                    elif self.selected_option == 2:  # Toggle musique
                        self.sound_manager.toggle_music()
                        self._update_options_text()
                        return SoundOptionAction.TOGGLE_MUSIC
                
                # Ajuster le volume
                elif event.key == pygame.K_LEFT:
                    if self.selected_option == 3:  # Volume des sons -
                        self.sound_manager.set_sound_volume(self.sound_manager.sound_volume - 0.1)
                        self.sound_manager.play_sound(SoundEffect.MENU_NAVIGATE)
                        return SoundOptionAction.SOUND_VOLUME_DOWN
                    elif self.selected_option == 4:  # Volume de la musique -
                        self.sound_manager.set_music_volume(self.sound_manager.music_volume - 0.1)
                        return SoundOptionAction.MUSIC_VOLUME_DOWN
                elif event.key == pygame.K_RIGHT:
                    if self.selected_option == 3:  # Volume des sons +
                        self.sound_manager.set_sound_volume(self.sound_manager.sound_volume + 0.1)
                        self.sound_manager.play_sound(SoundEffect.MENU_NAVIGATE)
                        return SoundOptionAction.SOUND_VOLUME_UP
                    elif self.selected_option == 4:  # Volume de la musique +
                        self.sound_manager.set_music_volume(self.sound_manager.music_volume + 0.1)
                        return SoundOptionAction.MUSIC_VOLUME_UP
        
        return None
    
    def draw(self, screen):
        """
        Dessine l'écran des options sonores.
        
        Args:
            screen (pygame.Surface): Surface de l'écran
        """
        # Effacer l'écran
        screen.fill(BLACK)
        
        # Titre
        title_text = self.title_font.render("Options Sonores", True, self.title_color)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
        screen.blit(title_text, title_rect)
        
        # Options
        for i, option in enumerate(self.options):
            # Ne pas afficher les textes des volumes ici, car ils ont une barre de progression
            if i == 3 or i == 4:
                text = option
            else:
                text = option
            
            color = self.selected_color if i == self.selected_option else self.option_color
            
            # Si les sons ou la musique sont désactivés, afficher en rouge
            if (i == 1 and not self.sound_manager.sound_enabled) or \
               (i == 2 and not self.sound_manager.music_enabled):
                color = self.disabled_color
            
            option_text = self.option_font.render(text, True, color)
            
            # Positionner les options
            if i == 0:  # Retour (en bas)
                option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 80))
            else:  # Autres options
                option_rect = option_text.get_rect(
                    x=WINDOW_WIDTH // 4,
                    y=WINDOW_HEIGHT // 3 + i * 50
                )
            
            screen.blit(option_text, option_rect)
            
            # Indicateur de sélection
            if i == self.selected_option:
                pygame.draw.circle(
                    screen, 
                    color, 
                    (option_rect.left - 15, option_rect.centery),
                    5
                )
        
        # Dessiner les barres de volume
        self._draw_volume_bar(
            screen, 
            self.sound_volume_rect, 
            self.sound_manager.sound_volume,
            self.selected_option == 3
        )
        
        self._draw_volume_bar(
            screen, 
            self.music_volume_rect, 
            self.sound_manager.music_volume,
            self.selected_option == 4
        )
    
    def _draw_volume_bar(self, screen, rect, value, selected):
        """
        Dessine une barre de volume.
        
        Args:
            screen (pygame.Surface): Surface de l'écran
            rect (pygame.Rect): Rectangle de la barre
            value (float): Valeur du volume (0.0 à 1.0)
            selected (bool): Indique si la barre est sélectionnée
        """
        # Dessiner le fond de la barre
        pygame.draw.rect(screen, WHITE, rect, 1)
        
        # Dessiner la partie remplie
        filled_rect = rect.copy()
        filled_rect.width = int(rect.width * value)
        pygame.draw.rect(
            screen, 
            self.selected_color if selected else WHITE, 
            filled_rect
        )
        
        # Afficher la valeur en pourcentage
        percent_text = self.option_font.render(f"{int(value * 100)}%", True, WHITE)
        percent_rect = percent_text.get_rect(
            midleft=(rect.right + 10, rect.centery)
        )
        screen.blit(percent_text, percent_rect)
