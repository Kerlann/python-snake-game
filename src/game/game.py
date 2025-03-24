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
from src.game.food import Food, FoodType
from src.game.score import Score
from src.game.level import Level
from src.ui.menu import Menu, MenuOption
from src.ui.game_over import GameOverScreen, GameOverOption
from src.ui.highscore_screen import HighScoreScreen, HighScoreScreenOption
from src.utils.highscore import HighScore

class GameState:
    """
    Énumération des états possibles du jeu.
    """
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    OPTIONS = 3
    HIGHSCORES = 4
    NAME_INPUT = 5
    QUIT = 6

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
        
        # Gestionnaire de meilleurs scores
        self.highscore_manager = HighScore()
        
        # Écran des meilleurs scores
        self.highscore_screen = HighScoreScreen(self.highscore_manager)
        
        # Création des objets du jeu
        self.reset_game()
        
        # Effets temporaires
        self.speed_effect_end_time = 0
        self.speed_multiplier = 1.0
        
    def reset_game(self):
        """
        Réinitialise le jeu pour une nouvelle partie.
        """
        # Création du système de niveaux
        self.level = Level()
        
        # Création du serpent
        self.snake = Snake()
        
        # Création de la nourriture
        self.food = Food(self.snake.body, level=self.level.current_level)
        
        # Création du score
        self.score = Score()
        
        # Écran de Game Over (sera créé quand nécessaire)
        self.game_over_screen = None
        
        # Timing pour le mouvement du serpent
        self.last_move_time = time.time()
        
        # Réinitialisation des effets
        self.speed_effect_end_time = 0
        self.speed_multiplier = 1.0
    
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
            elif option == MenuOption.HIGHSCORES:
                self.state = GameState.HIGHSCORES
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
        
        elif self.state == GameState.HIGHSCORES:
            option = self.highscore_screen.process_events(events)
            if option == HighScoreScreenOption.BACK:
                self.state = GameState.MENU
            elif option == HighScoreScreenOption.RESET:
                self.highscore_manager.reset_scores()
        
        elif self.state == GameState.NAME_INPUT:
            # Gérer la saisie du nom pour le meilleur score
            if self.highscore_manager.process_input(events):
                self.state = GameState.HIGHSCORES
        
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
            # Vérifier le passage au niveau suivant
            if self.level.check_level_up(self.score.value):
                # Annoncer le nouveau niveau (à implémenter)
                pass
            
            # Vérifier l'expiration des effets temporaires
            current_time = pygame.time.get_ticks()
            if current_time >= self.speed_effect_end_time:
                self.speed_multiplier = 1.0
            
            # Vérifier l'expiration de la nourriture spéciale
            if self.food.should_expire():
                self.food.respawn(
                    self.snake.body, 
                    self.level.obstacles,
                    self.level.current_level
                )
            
            # Calculer la vitesse actuelle du serpent
            current_speed = self.level.get_current_speed() * self.speed_multiplier
            
            # Déplacer le serpent à intervalle régulier
            current_time = time.time()
            if current_time - self.last_move_time > 1.0 / current_speed:
                # Vérifier si le serpent se heurte à un obstacle
                next_head_pos = self.snake.get_next_head_position()
                if self.level.check_obstacle_collision(next_head_pos):
                    self._handle_game_over()
                    return
                
                # Vérifier si le serpent a mangé de la nourriture
                if self.food.is_collision(self.snake.get_head_position()):
                    self.snake.grow()
                    
                    # Traiter les effets spéciaux de la nourriture
                    if self.food.type == FoodType.SPEED:
                        self.speed_multiplier = 1.5
                        self.speed_effect_end_time = pygame.time.get_ticks() + 5000  # 5 secondes
                    elif self.food.type == FoodType.SLOW:
                        self.speed_multiplier = 0.75
                        self.speed_effect_end_time = pygame.time.get_ticks() + 5000  # 5 secondes
                    
                    # Augmenter le score selon le type de nourriture
                    self.score.increase(self.food.get_points())
                    
                    # Générer une nouvelle nourriture
                    self.food.respawn(
                        self.snake.body, 
                        self.level.obstacles,
                        self.level.current_level
                    )
                
                # Déplacer le serpent
                if not self.snake.move():
                    self._handle_game_over()
                    return
                
                self.last_move_time = current_time
        
        elif self.state == GameState.GAME_OVER:
            self.game_over_screen.update(dt)
    
    def _handle_game_over(self):
        """
        Gère la fin de partie et vérifie les meilleurs scores.
        """
        # Vérifier si c'est un meilleur score
        if self.highscore_manager.is_high_score(self.score.value):
            # Demander le nom du joueur
            self.highscore_manager.start_input(self.score.value)
            self.state = GameState.NAME_INPUT
        else:
            # Afficher l'écran de game over normal
            self.game_over_screen = GameOverScreen(self.score.value)
            self.state = GameState.GAME_OVER
    
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
            # Dessiner les obstacles
            self.level.draw(self.screen)
            
            # Dessiner le serpent
            self.snake.draw(self.screen)
            
            # Dessiner la nourriture
            self.food.draw(self.screen)
            
            # Afficher le score
            self.score.draw(self.screen)
            
            # Afficher message de pause
            if self.paused:
                self._render_message("PAUSE - Appuyez sur P pour continuer", WHITE)
            
            # Afficher les effets actifs
            if pygame.time.get_ticks() < self.speed_effect_end_time:
                if self.speed_multiplier > 1.0:
                    self._render_message("VITESSE AUGMENTÉE!", WHITE, y_offset=30)
                else:
                    self._render_message("VITESSE RÉDUITE!", WHITE, y_offset=30)
        
        elif self.state == GameState.GAME_OVER:
            self.game_over_screen.draw(self.screen)
        
        elif self.state == GameState.HIGHSCORES:
            self.highscore_screen.draw(self.screen)
        
        elif self.state == GameState.NAME_INPUT:
            self.highscore_manager.draw_input(self.screen)
        
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
