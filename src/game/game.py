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
from src.game.food import Food
from src.game.score import Score
from src.ui.menu import Menu, MenuOption
from src.ui.game_over import GameOverScreen, GameOverOption

class GameState:
    """
    Énumération des états possibles du jeu.
    """
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    OPTIONS = 3
    QUIT = 4

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
        self.state = GameState.MENU
        self.running = True
        self.paused = False
        
        # Menu principal
        self.menu = Menu()
        
        # Création des objets du jeu
        self.reset_game()
        
    def reset_game(self):
        """
        Réinitialise le jeu pour une nouvelle partie.
        """
        # Création du serpent
        self.snake = Snake()
        
        # Création de la nourriture
        self.food = Food(self.snake.body)
        
        # Création du score
        self.score = Score()
        
        # Écran de Game Over (sera créé quand nécessaire)
        self.game_over_screen = None
        
        # Timing pour le mouvement du serpent
        self.last_move_time = time.time()
    
    def process_events(self):
        """
        Gère les événements Pygame (clavier, souris, etc.).
        """
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        
        # Traitement des événements selon l'état du jeu
        if self.state == GameState.MENU:
            option = self.menu.process_events(events)
            if option == MenuOption.PLAY:
                self.state = GameState.PLAYING
            elif option == MenuOption.OPTIONS:
                self.state = GameState.OPTIONS
            elif option == MenuOption.QUIT:
                self.running = False
                
        elif self.state == GameState.PLAYING:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    
                    # Contrôles du serpent
                    if not self.paused:
                        if event.key == pygame.K_UP:
                            self.snake.change_direction(Direction.UP)
                        elif event.key == pygame.K_DOWN:
                            self.snake.change_direction(Direction.DOWN)
                        elif event.key == pygame.K_LEFT:
                            self.snake.change_direction(Direction.LEFT)
                        elif event.key == pygame.K_RIGHT:
                            self.snake.change_direction(Direction.RIGHT)
        
        elif self.state == GameState.GAME_OVER:
            option = self.game_over_screen.process_events(events)
            if option == GameOverOption.PLAY_AGAIN:
                self.reset_game()
                self.state = GameState.PLAYING
            elif option == GameOverOption.MENU:
                self.state = GameState.MENU
            elif option == GameOverOption.QUIT:
                self.running = False
        
        elif self.state == GameState.OPTIONS:
            # Pour l'instant, juste retourner au menu
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
    
    def update(self):
        """
        Met à jour l'état du jeu.
        """
        dt = self.clock.get_time() / 1000.0  # Temps écoulé en secondes
        
        if self.state == GameState.MENU:
            self.menu.update(dt)
            
        elif self.state == GameState.PLAYING and not self.paused:
            # Déplacer le serpent à intervalle régulier
            current_time = time.time()
            if current_time - self.last_move_time > 1.0 / SNAKE_SPEED:
                # Vérifier si le serpent a mangé de la nourriture
                if self.food.is_collision(self.snake.get_head_position()):
                    self.snake.grow()
                    self.score.increase()
                    self.food.respawn(self.snake.body)
                
                # Déplacer le serpent
                if not self.snake.move():
                    self.game_over_screen = GameOverScreen(self.score.value)
                    self.state = GameState.GAME_OVER
                
                self.last_move_time = current_time
        
        elif self.state == GameState.GAME_OVER:
            self.game_over_screen.update(dt)
    
    def render(self):
        """
        Dessine les éléments du jeu sur l'écran.
        """
        # Effacer l'écran
        self.screen.fill(BLACK)
        
        # Rendu selon l'état du jeu
        if self.state == GameState.MENU:
            self.menu.draw(self.screen)
            
        elif self.state == GameState.PLAYING:
            # Dessiner le serpent
            self.snake.draw(self.screen)
            
            # Dessiner la nourriture
            self.food.draw(self.screen)
            
            # Afficher le score
            self.score.draw(self.screen)
            
            # Afficher message de pause
            if self.paused:
                self._render_message("PAUSE - Appuyez sur P pour continuer", WHITE)
        
        elif self.state == GameState.GAME_OVER:
            self.game_over_screen.draw(self.screen)
        
        elif self.state == GameState.OPTIONS:
            # Écran d'options simple
            self._render_message("OPTIONS - Appuyez sur ECHAP pour revenir au menu", WHITE)
        
        # Mise à jour de l'affichage
        pygame.display.flip()
    
    def _render_message(self, message, color, y_offset=0):
        """
        Affiche un message centré à l'écran.
        
        Args:
            message (str): Le message à afficher
            color (tuple): La couleur RGB du texte
            y_offset (int, optional): Décalage vertical par rapport au centre. Par défaut 0.
        """
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + y_offset))
        self.screen.blit(text, text_rect)
    
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
