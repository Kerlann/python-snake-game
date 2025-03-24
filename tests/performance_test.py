"""
Script pour tester les performances du jeu.
"""

import sys
import os
import time
import cProfile
import pstats

# Ajouter le répertoire parent au chemin de recherche pour importer le module src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from src.game.snake import Snake, Direction
from src.game.food import Food
from src.game.level import Level
from src.utils.logger import Logger

# Initialisation du logger
logger = Logger(name='performance_test', level=20)  # INFO = 20

# Initialisation de Pygame
pygame.init()
screen = pygame.Surface((800, 600))  # Surface hors écran pour les tests

def test_snake_move(iterations=1000):
    """
    Teste les performances de la méthode move() de Snake.
    
    Args:
        iterations (int): Nombre d'itérations à exécuter
    """
    logger.info(f"Test de Snake.move() avec {iterations} itérations")
    
    # Créer un serpent
    snake = Snake()
    
    # Mesurer le temps d'exécution
    start_time = time.time()
    
    for i in range(iterations):
        snake.move()
        
        # Changer de direction périodiquement pour éviter de sortir des limites
        if i % 10 == 0:
            snake.change_direction(Direction.UP)
        elif i % 20 == 0:
            snake.change_direction(Direction.RIGHT)
        elif i % 30 == 0:
            snake.change_direction(Direction.DOWN)
        elif i % 40 == 0:
            snake.change_direction(Direction.LEFT)
    
    elapsed_time = time.time() - start_time
    
    logger.info(f"Temps d'exécution: {elapsed_time:.6f} secondes")
    logger.info(f"Moyenne par itération: {(elapsed_time / iterations) * 1000:.6f} ms")
    
    return elapsed_time

def test_food_respawn(iterations=1000):
    """
    Teste les performances de la méthode respawn() de Food.
    
    Args:
        iterations (int): Nombre d'itérations à exécuter
    """
    logger.info(f"Test de Food.respawn() avec {iterations} itérations")
    
    # Créer un serpent et une nourriture
    snake = Snake()
    food = Food(snake.body)
    
    # Mesurer le temps d'exécution
    start_time = time.time()
    
    for _ in range(iterations):
        food.respawn(snake.body)
    
    elapsed_time = time.time() - start_time
    
    logger.info(f"Temps d'exécution: {elapsed_time:.6f} secondes")
    logger.info(f"Moyenne par itération: {(elapsed_time / iterations) * 1000:.6f} ms")
    
    return elapsed_time

def test_obstacle_generation(iterations=100):
    """
    Teste les performances de la méthode generate_obstacles() de Level.
    
    Args:
        iterations (int): Nombre d'itérations à exécuter
    """
    logger.info(f"Test de Level.generate_obstacles() avec {iterations} itérations")
    
    # Créer un niveau
    level = Level()
    level.current_level = 3  # Pour avoir des obstacles
    
    # Mesurer le temps d'exécution
    start_time = time.time()
    
    for _ in range(iterations):
        level.generate_obstacles()
    
    elapsed_time = time.time() - start_time
    
    logger.info(f"Temps d'exécution: {elapsed_time:.6f} secondes")
    logger.info(f"Moyenne par itération: {(elapsed_time / iterations) * 1000:.6f} ms")
    
    return elapsed_time

def profile_game_update():
    """
    Profile la méthode update() du jeu pour identifier les goulots d'étranglement.
    """
    logger.info("Profiling de Game.update()")
    
    # Importer Game ici pour éviter les imports circulaires
    from src.game.game import Game
    
    # Créer une instance du jeu
    game = Game()
    game.state = 1  # GameState.PLAYING
    
    # Profiler
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Simuler plusieurs mises à jour
    for _ in range(1000):
        game.update()
    
    profiler.disable()
    
    # Enregistrer les résultats
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "profile_results.txt")
    stats.dump_stats(os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "profile_results.prof"))
    
    with open(stats_file, 'w') as f:
        stats_stream = pstats.Stream(f)
        stats.print_stats(100, stats_stream)  # Afficher les 100 premières entrées
    
    logger.info(f"Résultats du profiling enregistrés dans {stats_file}")

if __name__ == '__main__':
    logger.info("Début des tests de performance")
    
    # Exécuter les tests
    test_snake_move()
    test_food_respawn()
    test_obstacle_generation()
    
    # Profiler le jeu
    profile_game_update()
    
    logger.info("Fin des tests de performance")
