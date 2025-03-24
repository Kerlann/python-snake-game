"""
Module principal contenant la classe Game qui gère le cycle de vie du jeu Snake.
"""

import pygame
import sys
import time
import logging
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
from src.ui.sound_options import SoundOptions, SoundOptionAction
from src.utils.highscore import HighScore
from src.utils.sound_manager import SoundManager, SoundEffect
from src.utils.logger import Logger

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
    SOUND_OPTIONS = 6
    QUIT = 7

class Game:
    """
    Classe principale du jeu qui gère le cycle de vie et les états du jeu.
    """
    
    def __init__(self, debug_mode=False):
        """
        Initialise une nouvelle instance du jeu.
        
        Args:
            debug_mode (bool, optional): Indique si le mode débogage est activé. Par défaut False.
        """
        # Initialisation du logger
        log_level = logging.DEBUG if debug_mode else logging.INFO
        self.logger = Logger(name='snake_game', level=log_level)
        self.logger.info("Initialisation du jeu Snake")
        
        # Initialisation de Pygame
        pygame.init()
        
        # Création de la fenêtre
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.logger.info(f"Fenêtre créée ({WINDOW_WIDTH}x{WINDOW_HEIGHT})")
        
        # Horloge pour contrôler le FPS
        self.clock = pygame.time.Clock()
        
        # État du jeu
        self.state = GameState.MENU
        self.running = True
        self.paused = False
        
        # Mode débogage
        self.debug_mode = debug_mode
        
        # Menu principal
        self.menu = Menu()
        
        # Gestionnaire de meilleurs scores
        self.highscore_manager = HighScore()
        
        # Écran des meilleurs scores
        self.highscore_screen = HighScoreScreen(self.highscore_manager)
        
        # Gestionnaire de sons
        self.sound_manager = SoundManager()
        
        # Écran des options sonores
        self.sound_options = SoundOptions(self.sound_manager)
        
        # Pour les tests, créer des sons placeholders
        self.sound_manager.create_placeholder_sounds()
        
        # Lancer la musique du menu
        self.sound_manager.play_music()
        
        # Création des objets du jeu
        self.reset_game()
        
        # Effets temporaires
        self.speed_effect_end_time = 0
        self.speed_multiplier = 1.0
        
        # Statistiques de performance
        self.frame_times = []
        self.max_frame_times = 100  # Pour calculer une moyenne sur les 100 dernières frames
        
        self.logger.info("Initialisation du jeu terminée")
        
    def reset_game(self):
        """
        Réinitialise le jeu pour une nouvelle partie.
        """
        self.logger.info("Réinitialisation du jeu")
        
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
        
        # Changer la musique pour le jeu
        if self.state == GameState.PLAYING:
            self.sound_manager.play_music("game_background.wav")
    
    def process_events(self):
        """
        Gère les événements Pygame (clavier, souris, etc.).
        """
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.logger.info("Événement QUIT détecté")
                self.running = False
        
        # Traitement des événements selon l'état du jeu
        if self.state == GameState.MENU:
            option = self.menu.process_events(events)
            if option == MenuOption.PLAY:
                self.logger.info("Lancement du jeu depuis le menu")
                self.reset_game()
                self.state = GameState.PLAYING
                self.sound_manager.play_sound(SoundEffect.MENU_SELECT)
                self.sound_manager.play_music("game_background.wav")
            elif option == MenuOption.HIGHSCORES:
                self.logger.info("Accès aux meilleurs scores depuis le menu")
                self.state = GameState.HIGHSCORES
                self.sound_manager.play_sound(SoundEffect.MENU_SELECT)
            elif option == MenuOption.OPTIONS:
                self.logger.info("Accès aux options sonores depuis le menu")
                self.state = GameState.SOUND_OPTIONS
                self.sound_manager.play_sound(SoundEffect.MENU_SELECT)
            elif option == MenuOption.QUIT:
                self.logger.info("Quitter le jeu depuis le menu")
                self.running = False
                self.sound_manager.play_sound(SoundEffect.MENU_SELECT)
                
        elif self.state == GameState.PLAYING:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.logger.info("Retour au menu depuis le jeu")
                        self.state = GameState.MENU
                        self.sound_manager.play_music()  # Retour à la musique du menu
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                        self.logger.info(f"Jeu {'en pause' if self.paused else 'repris'}")
                    
                    # Contrôles du serpent
                    if not self.paused:
                        direction_changed = False
                        if event.key == pygame.K_UP:
                            self.snake.change_direction(Direction.UP)
                            direction_changed = True
                        elif event.key == pygame.K_DOWN:
                            self.snake.change_direction(Direction.DOWN)
                            direction_changed = True
                        elif event.key == pygame.K_LEFT:
                            self.snake.change_direction(Direction.LEFT)
                            direction_changed = True
                        elif event.key == pygame.K_RIGHT:
                            self.snake.change_direction(Direction.RIGHT)
                            direction_changed = True
                            
                        if direction_changed:
                            self.logger.debug(f"Direction du serpent changée: {self.snake.direction}")
                            self.sound_manager.play_sound(SoundEffect.MOVE)
        
        elif self.state == GameState.GAME_OVER:
            option = self.game_over_screen.process_events(events)
            if option == GameOverOption.PLAY_AGAIN:
                self.logger.info("Nouvelle partie depuis l'écran de Game Over")
                self.reset_game()
                self.state = GameState.PLAYING
                self.sound_manager.play_sound(SoundEffect.MENU_SELECT)
                self.sound_manager.play_music("game_background.wav")
            elif option == GameOverOption.MENU:
                self.logger.info("Retour au menu depuis l'écran de Game Over")
                self.state = GameState.MENU
                self.sound_manager.play_sound(SoundEffect.MENU_SELECT)
                self.sound_manager.play_music()  # Retour à la musique du menu
            elif option == GameOverOption.QUIT:
                self.logger.info("Quitter le jeu depuis l'écran de Game Over")
                self.running = False
                self.sound_manager.play_sound(SoundEffect.MENU_SELECT)
        
        elif self.state == GameState.HIGHSCORES:
            option = self.highscore_screen.process_events(events)
            if option == HighScoreScreenOption.BACK:
                self.logger.info("Retour au menu depuis l'écran des meilleurs scores")
                self.state = GameState.MENU
                self.sound_manager.play_sound(SoundEffect.MENU_SELECT)
            elif option == HighScoreScreenOption.RESET:
                self.logger.info("Réinitialisation des meilleurs scores")
                self.highscore_manager.reset_scores()
                self.sound_manager.play_sound(SoundEffect.MENU_SELECT)
        
        elif self.state == GameState.NAME_INPUT:
            # Gérer la saisie du nom pour le meilleur score
            if self.highscore_manager.process_input(events):
                self.logger.info("Nom saisi pour le meilleur score")
                self.state = GameState.HIGHSCORES
        
        elif self.state == GameState.SOUND_OPTIONS:
            option = self.sound_options.process_events(events)
            if option == SoundOptionAction.BACK:
                self.logger.info("Retour au menu depuis les options sonores")
                self.state = GameState.MENU
        
        elif self.state == GameState.OPTIONS:
            # Pour l'instant, juste retourner au menu
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.logger.info("Retour au menu depuis les options")
                        self.state = GameState.MENU
                        self.sound_manager.play_sound(SoundEffect.MENU_SELECT)
    
    def update(self):
        """
        Met à jour l'état du jeu.
        """
        dt = self.clock.get_time() / 1000.0  # Temps écoulé en secondes
        
        # Mesurer le temps de frame pour les statistiques
        start_time = time.time()
        
        if self.state == GameState.MENU:
            self.menu.update(dt)
            
        elif self.state == GameState.PLAYING and not self.paused:
            # Vérifier le passage au niveau suivant
            if self.level.check_level_up(self.score.value):
                self.logger.info(f"Niveau suivant! Niveau {self.level.current_level}")
                # Jouer le son de passage de niveau
                self.sound_manager.play_sound(SoundEffect.LEVEL_UP)
            
            # Vérifier l'expiration des effets temporaires
            current_time = pygame.time.get_ticks()
            if current_time >= self.speed_effect_end_time:
                if self.speed_multiplier != 1.0:
                    self.logger.debug("Fin de l'effet de vitesse")
                    self.speed_multiplier = 1.0
            
            # Vérifier l'expiration de la nourriture spéciale
            if self.food.should_expire():
                self.logger.debug("Nourriture expirée, respawn")
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
                    self.logger.info(f"Collision avec un obstacle à {next_head_pos}")
                    self._handle_game_over()
                    return
                
                # Vérifier si le serpent a mangé de la nourriture
                if self.food.is_collision(self.snake.get_head_position()):
                    self.snake.grow()
                    self.logger.info(f"Nourriture mangée de type {self.food.type}, score: {self.score.value}")
                    
                    # Jouer le son de consommation de nourriture
                    self.sound_manager.play_sound(SoundEffect.EAT)
                    
                    # Traiter les effets spéciaux de la nourriture
                    if self.food.type == FoodType.SPEED:
                        self.logger.debug("Effet de vitesse augmentée activé")
                        self.speed_multiplier = 1.5
                        self.speed_effect_end_time = pygame.time.get_ticks() + 5000  # 5 secondes
                    elif self.food.type == FoodType.SLOW:
                        self.logger.debug("Effet de vitesse réduite activé")
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
                    self.logger.info(f"Collision fatale du serpent, score final: {self.score.value}")
                    self._handle_game_over()
                    return
                
                self.last_move_time = current_time
        
        elif self.state == GameState.GAME_OVER:
            self.game_over_screen.update(dt)
        
        # Calculer le temps de frame
        frame_time = time.time() - start_time
        self.frame_times.append(frame_time)
        
        # Limiter la taille de la liste des temps de frame
        if len(self.frame_times) > self.max_frame_times:
            self.frame_times.pop(0)
        
        # Logger les statistiques de performance en mode débogage
        if self.debug_mode and len(self.frame_times) >= 10:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.logger.debug(f"Temps moyen de frame: {avg_frame_time * 1000:.2f} ms, FPS: {1.0 / avg_frame_time:.1f}")
    
    def _handle_game_over(self):
        """
        Gère la fin de partie et vérifie les meilleurs scores.
        """
        # Jouer le son de game over
        self.sound_manager.play_sound(SoundEffect.GAME_OVER)
        
        # Changer pour la musique du menu
        self.sound_manager.play_music()
        
        # Vérifier si c'est un meilleur score
        if self.highscore_manager.is_high_score(self.score.value):
            self.logger.info("Nouveau meilleur score! Demande du nom du joueur")
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
            
            # Afficher les informations de débogage
            if self.debug_mode:
                self._render_debug_info()
        
        elif self.state == GameState.GAME_OVER:
            self.game_over_screen.draw(self.screen)
        
        elif self.state == GameState.HIGHSCORES:
            self.highscore_screen.draw(self.screen)
        
        elif self.state == GameState.NAME_INPUT:
            self.highscore_manager.draw_input(self.screen)
        
        elif self.state == GameState.SOUND_OPTIONS:
            self.sound_options.draw(self.screen)
        
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
    
    def _render_debug_info(self):
        """
        Affiche des informations de débogage sur l'écran.
        """
        debug_font = pygame.font.Font(None, 20)
        y_pos = 10
        
        # FPS
        fps = int(self.clock.get_fps())
        fps_text = debug_font.render(f"FPS: {fps}", True, WHITE)
        self.screen.blit(fps_text, (WINDOW_WIDTH - fps_text.get_width() - 10, y_pos))
        y_pos += 20
        
        # Taille du serpent
        snake_length = len(self.snake.body)
        snake_text = debug_font.render(f"Taille serpent: {snake_length}", True, WHITE)
        self.screen.blit(snake_text, (WINDOW_WIDTH - snake_text.get_width() - 10, y_pos))
        y_pos += 20
        
        # Niveau et score
        level_text = debug_font.render(f"Niveau: {self.level.current_level} | Score: {self.score.value}", True, WHITE)
        self.screen.blit(level_text, (WINDOW_WIDTH - level_text.get_width() - 10, y_pos))
        y_pos += 20
        
        # Type de nourriture
        food_text = debug_font.render(f"Nourriture: {self.food.type.name}", True, WHITE)
        self.screen.blit(food_text, (WINDOW_WIDTH - food_text.get_width() - 10, y_pos))
    
    def run(self):
        """
        Boucle principale du jeu.
        """
        self.logger.info("Démarrage de la boucle principale du jeu")
        try:
            while self.running:
                self.process_events()
                self.update()
                self.render()
                self.clock.tick(FPS)
            
            self.logger.info("Fin de la boucle principale, arrêt du jeu")
        except Exception as e:
            self.logger.critical(f"Erreur fatale pendant l'exécution du jeu: {e}")
            import traceback
            self.logger.critical(traceback.format_exc())
        finally:
            # Nettoyage avant de quitter
            pygame.quit()
            sys.exit()
