"""
Module principal contenant la classe Game qui gère le cycle de vie du jeu Snake.
"""

import pygame
import sys
import time
from src.utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, 
    FPS, GAME_TITLE, SNAKE_SPEED
)
from src.game.snake import Snake, Direction

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
        
        # Création du serpent
        self.snake = Snake()
        
        # État du jeu
        self.running = True
        self.paused = False
        self.game_over = False
        
        # Timing pour le mouvement du serpent
        self.last_move_time = time.time()
        
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
                
                # Contrôles du serpent
                if not self.game_over:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(Direction.RIGHT)
                
                # Redémarrer le jeu si Game Over
                if self.game_over and event.key == pygame.K_SPACE:
                    self.reset_game()
    
    def update(self):
        """
        Met à jour l'état du jeu.
        """
        if not self.paused and not self.game_over:
            # Déplacer le serpent à intervalle régulier
            current_time = time.time()
            if current_time - self.last_move_time > 1.0 / SNAKE_SPEED:
                if not self.snake.move():
                    self.game_over = True
                self.last_move_time = current_time
    
    def render(self):
        """
        Dessine les éléments du jeu sur l'écran.
        """
        # Effacer l'écran
        self.screen.fill(BLACK)
        
        # Dessiner le serpent
        self.snake.draw(self.screen)
        
        # Afficher message de pause ou de game over
        if self.paused:
            self._render_message("PAUSE - Appuyez sur P pour continuer", WHITE)
        elif self.game_over:
            self._render_message("GAME OVER - Appuyez sur ESPACE pour recommencer", WHITE)
        
        # Mise à jour de l'affichage
        pygame.display.flip()
    
    def _render_message(self, message, color):
        """
        Affiche un message centré à l'écran.
        
        Args:
            message (str): Le message à afficher
            color (tuple): La couleur RGB du texte
        """
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(text, text_rect)
    
    def reset_game(self):
        """
        Réinitialise le jeu pour une nouvelle partie.
        """
        self.snake = Snake()
        self.game_over = False
        self.paused = False
    
    def run(self):
        """
        Boucle principale du jeu.
        """
        while self.running:
            self.process_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        # Nettoyage avant de quitter
        pygame.quit()
        sys.exit()
