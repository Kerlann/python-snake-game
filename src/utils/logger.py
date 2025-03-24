"""
Module pour la journalisation (logging) dans le jeu.
"""

import os
import logging
from datetime import datetime

class Logger:
    """
    Classe pour gérer la journalisation dans le jeu.
    """
    
    def __init__(self, name='snake_game', level=logging.INFO):
        """
        Initialise un logger.
        
        Args:
            name (str, optional): Nom du logger. Par défaut 'snake_game'.
            level (int, optional): Niveau de journalisation. Par défaut logging.INFO.
        """
        # Créer le dossier de logs s'il n'existe pas
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        # Format du nom de fichier avec la date et l'heure
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(logs_dir, f"{name}_{current_time}.log")
        
        # Configurer le logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Handler pour les fichiers
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        
        # Handler pour la console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # Format des messages
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Ajouter les handlers au logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info(f"Logger initialisé dans {log_file}")
    
    def debug(self, message):
        """
        Enregistre un message de débogage.
        
        Args:
            message (str): Message à enregistrer
        """
        self.logger.debug(message)
    
    def info(self, message):
        """
        Enregistre un message d'information.
        
        Args:
            message (str): Message à enregistrer
        """
        self.logger.info(message)
    
    def warning(self, message):
        """
        Enregistre un message d'avertissement.
        
        Args:
            message (str): Message à enregistrer
        """
        self.logger.warning(message)
    
    def error(self, message):
        """
        Enregistre un message d'erreur.
        
        Args:
            message (str): Message à enregistrer
        """
        self.logger.error(message)
    
    def critical(self, message):
        """
        Enregistre un message critique.
        
        Args:
            message (str): Message à enregistrer
        """
        self.logger.critical(message)
