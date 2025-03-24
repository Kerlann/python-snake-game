"""
Module contenant la classe HighScore qui gère les meilleurs scores.
"""

import os
import json
import pygame
from src.utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, GREEN
)

class HighScore:
    """
    Classe gérant la sauvegarde et l'affichage des meilleurs scores.
    """
    
    def __init__(self, filename="highscores.json"):
        """
        Initialise un gestionnaire de meilleurs scores.
        
        Args:
            filename (str, optional): Nom du fichier de sauvegarde. Par défaut "highscores.json".
        """
        self.filename = filename
        self.scores = []
        self.max_scores = 10  # Nombre maximum de scores à conserver
        
        # Polices pour l'affichage
        self.title_font = pygame.font.Font(None, 48)
        self.score_font = pygame.font.Font(None, 36)
        self.input_font = pygame.font.Font(None, 32)
        
        # État pour la saisie du nom
        self.input_active = False
        self.current_name = ""
        self.current_score = 0
        self.input_rect = pygame.Rect(
            WINDOW_WIDTH // 2 - 100, 
            WINDOW_HEIGHT // 2, 
            200, 
            32
        )
        
        # Charger les scores existants
        self.load()
    
    def load(self):
        """
        Charge les meilleurs scores à partir d'un fichier JSON.
        """
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.scores = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erreur lors du chargement des meilleurs scores: {e}")
            self.scores = []
    
    def save(self):
        """
        Sauvegarde les meilleurs scores dans un fichier JSON.
        """
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.scores, f)
        except IOError as e:
            print(f"Erreur lors de la sauvegarde des meilleurs scores: {e}")
    
    def is_high_score(self, score):
        """
        Vérifie si un score peut entrer dans les meilleurs scores.
        
        Args:
            score (int): Score à vérifier
            
        Returns:
            bool: True si c'est un meilleur score, False sinon
        """
        if len(self.scores) < self.max_scores:
            return True
        return any(score > s["score"] for s in self.scores)
    
    def add_score(self, name, score):
        """
        Ajoute un nouveau score à la liste des meilleurs scores.
        
        Args:
            name (str): Nom du joueur
            score (int): Score obtenu
        """
        # Ajouter le nouveau score
        self.scores.append({"name": name, "score": score})
        
        # Trier les scores par ordre décroissant
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        
        # Limiter le nombre de scores
        if len(self.scores) > self.max_scores:
            self.scores = self.scores[:self.max_scores]
        
        # Sauvegarder les scores
        self.save()
    
    def start_input(self, score):
        """
        Démarre la saisie du nom pour un nouveau meilleur score.
        
        Args:
            score (int): Score obtenu
        """
        self.input_active = True
        self.current_name = ""
        self.current_score = score
    
    def process_input(self, events):
        """
        Traite les événements de saisie du nom.
        
        Args:
            events (list): Liste des événements Pygame
            
        Returns:
            bool: True si la saisie est terminée, False sinon
        """
        if not self.input_active:
            return False
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Terminer la saisie
                    if self.current_name.strip():
                        self.add_score(self.current_name, self.current_score)
                        self.input_active = False
                        return True
                elif event.key == pygame.K_BACKSPACE:
                    # Supprimer le dernier caractère
                    self.current_name = self.current_name[:-1]
                else:
                    # Ajouter un caractère (limité à 10)
                    if len(self.current_name) < 10 and event.unicode.isprintable():
                        self.current_name += event.unicode
        
        return False
    
    def reset_scores(self):
        """
        Réinitialise la liste des meilleurs scores.
        """
        self.scores = []
        self.save()
    
    def draw_high_scores(self, screen):
        """
        Affiche la liste des meilleurs scores sur l'écran.
        
        Args:
            screen (pygame.Surface): Surface de l'écran
        """
        # Effacer l'écran
        screen.fill(BLACK)
        
        # Titre
        title_text = self.title_font.render("Meilleurs Scores", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        # Dessiner les scores
        if not self.scores:
            # Pas de scores enregistrés
            no_score_text = self.score_font.render("Aucun score enregistré", True, WHITE)
            no_score_rect = no_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(no_score_text, no_score_rect)
        else:
            for i, entry in enumerate(self.scores):
                # Position du texte
                y_pos = 120 + i * 40
                
                # Afficher le rang
                rank_text = self.score_font.render(f"{i+1}.", True, WHITE)
                screen.blit(rank_text, (WINDOW_WIDTH // 4, y_pos))
                
                # Afficher le nom
                name_text = self.score_font.render(entry["name"], True, WHITE)
                screen.blit(name_text, (WINDOW_WIDTH // 4 + 50, y_pos))
                
                # Afficher le score
                score_text = self.score_font.render(str(entry["score"]), True, WHITE)
                score_rect = score_text.get_rect(right=WINDOW_WIDTH * 3 // 4)
                screen.blit(score_text, (score_rect.x, y_pos))
        
        # Instructions
        instruction_text = self.score_font.render("Appuyez sur ECHAP pour revenir", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        screen.blit(instruction_text, instruction_rect)
    
    def draw_input(self, screen):
        """
        Affiche l'écran de saisie du nom pour un nouveau meilleur score.
        
        Args:
            screen (pygame.Surface): Surface de l'écran
        """
        if not self.input_active:
            return
        
        # Effacer l'écran
        screen.fill(BLACK)
        
        # Titre
        title_text = self.title_font.render("Nouveau Meilleur Score!", True, GREEN)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        screen.blit(title_text, title_rect)
        
        # Score
        score_text = self.score_font.render(f"Score: {self.current_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 50))
        screen.blit(score_text, score_rect)
        
        # Instruction
        instruction_text = self.score_font.render("Entrez votre nom:", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        screen.blit(instruction_text, instruction_rect)
        
        # Champ de saisie
        pygame.draw.rect(screen, WHITE, self.input_rect, 2)
        text_surface = self.input_font.render(self.current_name, True, WHITE)
        screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        
        # Instruction de validation
        enter_text = self.input_font.render("Appuyez sur ENTRÉE pour valider", True, WHITE)
        enter_rect = enter_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        screen.blit(enter_text, enter_rect)
