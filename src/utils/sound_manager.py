"""
Module contenant la classe SoundManager qui gère les sons et la musique du jeu.
"""

import os
import pygame

class SoundEffect:
    """
    Énumération des effets sonores disponibles.
    """
    MOVE = "move"
    EAT = "eat"
    GAME_OVER = "game_over"
    LEVEL_UP = "level_up"
    MENU_SELECT = "menu_select"
    MENU_NAVIGATE = "menu_navigate"


class SoundManager:
    """
    Classe gérant les sons et la musique du jeu.
    """
    
    def __init__(self):
        """
        Initialise un nouveau gestionnaire de sons.
        """
        # Initialiser le module de son de Pygame
        pygame.mixer.init()
        
        # Créer les dossiers de sons s'ils n'existent pas
        self.sound_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "sounds")
        self.music_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "music")
        
        os.makedirs(self.sound_dir, exist_ok=True)
        os.makedirs(self.music_dir, exist_ok=True)
        
        # Dictionnaire pour stocker les sons
        self.sounds = {}
        
        # Paramètres
        self.sound_volume = 0.7  # 70% du volume max
        self.music_volume = 0.5  # 50% du volume max
        self.sound_enabled = True
        self.music_enabled = True
        
        # Chargez les sons (s'ils existent)
        self._load_sounds()
    
    def _load_sounds(self):
        """
        Charge les sons à partir des fichiers.
        """
        # Assurez-vous que le dossier existe
        if not os.path.exists(self.sound_dir):
            print(f"Dossier de sons non trouvé: {self.sound_dir}")
            return
        
        # Définir les mappages des noms de fichiers
        sound_files = {
            SoundEffect.MOVE: "move.wav",
            SoundEffect.EAT: "eat.wav",
            SoundEffect.GAME_OVER: "game_over.wav",
            SoundEffect.LEVEL_UP: "level_up.wav",
            SoundEffect.MENU_SELECT: "menu_select.wav",
            SoundEffect.MENU_NAVIGATE: "menu_navigate.wav"
        }
        
        # Charger chaque son
        for sound_name, file_name in sound_files.items():
            file_path = os.path.join(self.sound_dir, file_name)
            if os.path.exists(file_path):
                try:
                    sound = pygame.mixer.Sound(file_path)
                    sound.set_volume(self.sound_volume)
                    self.sounds[sound_name] = sound
                except pygame.error as e:
                    print(f"Erreur lors du chargement du son {file_name}: {e}")
            else:
                print(f"Fichier son non trouvé: {file_path}")
    
    def play_sound(self, sound_name):
        """
        Joue un effet sonore.
        
        Args:
            sound_name (SoundEffect): Nom de l'effet sonore à jouer
        """
        if not self.sound_enabled:
            return
        
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_music(self, music_name="background.mp3", loop=True):
        """
        Joue de la musique en arrière-plan.
        
        Args:
            music_name (str, optional): Nom du fichier de musique. Par défaut "background.mp3".
            loop (bool, optional): Indique si la musique doit être jouée en boucle. Par défaut True.
        """
        if not self.music_enabled:
            return
        
        # Arrêter la musique en cours
        pygame.mixer.music.stop()
        
        # Charger et jouer la nouvelle musique
        music_path = os.path.join(self.music_dir, music_name)
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1 if loop else 0)
            except pygame.error as e:
                print(f"Erreur lors du chargement de la musique {music_name}: {e}")
        else:
            print(f"Fichier de musique non trouvé: {music_path}")
    
    def stop_music(self):
        """
        Arrête la musique en cours.
        """
        pygame.mixer.music.stop()
    
    def toggle_sound(self):
        """
        Active/désactive les effets sonores.
        
        Returns:
            bool: Nouvel état des effets sonores
        """
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled
    
    def toggle_music(self):
        """
        Active/désactive la musique.
        
        Returns:
            bool: Nouvel état de la musique
        """
        self.music_enabled = not self.music_enabled
        
        if self.music_enabled:
            # Reprendre la musique
            pygame.mixer.music.unpause()
        else:
            # Mettre en pause la musique
            pygame.mixer.music.pause()
            
        return self.music_enabled
    
    def set_sound_volume(self, volume):
        """
        Règle le volume des effets sonores.
        
        Args:
            volume (float): Nouveau volume (0.0 à 1.0)
        """
        # Limiter le volume entre 0 et 1
        self.sound_volume = max(0.0, min(1.0, volume))
        
        # Mettre à jour le volume de tous les sons
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume):
        """
        Règle le volume de la musique.
        
        Args:
            volume (float): Nouveau volume (0.0 à 1.0)
        """
        # Limiter le volume entre 0 et 1
        self.music_volume = max(0.0, min(1.0, volume))
        
        # Mettre à jour le volume de la musique
        pygame.mixer.music.set_volume(self.music_volume)
    
    def create_placeholder_sounds(self):
        """
        Crée des fichiers sons vides pour les tests.
        Cette méthode est utile pour le développement.
        """
        import wave
        import struct
        
        # S'assurer que les dossiers existent
        os.makedirs(self.sound_dir, exist_ok=True)
        os.makedirs(self.music_dir, exist_ok=True)
        
        # Créer un son simple pour chaque effet
        for sound_name in [
            "move.wav", "eat.wav", "game_over.wav", 
            "level_up.wav", "menu_select.wav", "menu_navigate.wav"
        ]:
            file_path = os.path.join(self.sound_dir, sound_name)
            
            # Créer un fichier WAV vide
            with wave.open(file_path, "w") as f:
                f.setnchannels(1)  # Mono
                f.setsampwidth(2)  # 16 bits
                f.setframerate(44100)  # 44.1 kHz
                
                # Générer un bip court
                duration = 0.2  # secondes
                frequency = 440  # Hz (note A4)
                
                # Différentes fréquences pour différents sons
                if "move" in sound_name:
                    frequency = 300
                elif "eat" in sound_name:
                    frequency = 600
                elif "game_over" in sound_name:
                    frequency = 200
                elif "level_up" in sound_name:
                    frequency = 800
                elif "menu" in sound_name:
                    frequency = 500
                
                # Générer les données audio
                num_frames = int(duration * 44100)
                data = []
                for i in range(num_frames):
                    t = float(i) / 44100  # Temps en secondes
                    value = int(32767 * 0.5 * (
                        1 if i < num_frames // 2 else 0
                    ) * (1 - t / duration))
                    data.append(struct.pack('<h', value))
                
                f.writeframes(b''.join(data))
        
        # Créer un fichier de musique simple (utiliser un WAV pour la simplicité)
        music_path = os.path.join(self.music_dir, "background.wav")
        with wave.open(music_path, "w") as f:
            f.setnchannels(1)  # Mono
            f.setsampwidth(2)  # 16 bits
            f.setframerate(44100)  # 44.1 kHz
            
            # Générer une boucle simple
            duration = 5.0  # secondes
            frequency = 260  # Hz (note C4)
            
            # Générer les données audio
            num_frames = int(duration * 44100)
            data = []
            for i in range(num_frames):
                t = float(i) / 44100  # Temps en secondes
                value = int(16384 * 0.5 * (
                    0.5 + 0.5 * ((t * frequency) % 1 > 0.5)
                ))
                data.append(struct.pack('<h', value))
            
            f.writeframes(b''.join(data))
