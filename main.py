#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Jeu Snake en Python avec Pygame
Point d'entrée principal du programme
"""

from src.game.game import Game

def main():
    """
    Fonction principale qui initialise et lance le jeu.
    """
    print("Initialisation du jeu Snake...")
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
