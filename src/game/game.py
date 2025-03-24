"""
Module principal contenant la classe Game qui gère le cycle de vie du jeu Snake.
"""

import pygame
import sys
from src.utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, 
    FPS, GAME_TITLE
)

class Game:
    """
    Classe principale du jeu qui gère le cycle de vie et les états du jeu.
    """
    
    def __init__(self):
        """
        Initialise une nouvelle instance du jeu.
        """
        # Initialisation de Pygame
        pygame.init()
        
        # Création de la fenêtre
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        
        # Horloge pour contrôler le FPS
        self.clock = pygame.time.Clock()
        
        # État du jeu
        self.running = True
        self.paused = False
        
    def process_events(self):
        """
        Gère les événements Pygame (clavier, souris, etc.).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
    
    def update(self):
        """
        Met à jour l'état du jeu.
        """
        if not self.paused:
            # Les mises à jour du jeu seront ajoutées ici
            pass
    
    def render(self):
        """
        Dessine les éléments du jeu sur l'écran.
        """
        # Effacer l'écran
        self.screen.fill(BLACK)
        
        # Dessiner les éléments du jeu ici
        # ...
        
        # Mise à jour de l'affichage
        pygame.display.flip()
    
    def run(self):
        """
        Boucle principale du jeu.
        """
        while self.running:
            self.process_events()
            if not self.paused:
                self.update()
            self.render()
            self.clock.tick(FPS)
        
        # Nettoyage avant de quitter
        pygame.quit()
        sys.exit()
