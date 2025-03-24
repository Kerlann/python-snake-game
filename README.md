# Jeu Snake en Python

Un jeu Snake classique développé en Python avec la bibliothèque Pygame.

## Description

Ce projet est une implémentation du jeu classique Snake où le joueur contrôle un serpent qui grandit en mangeant des pommes. Le jeu se termine lorsque le serpent se heurte à lui-même ou aux murs.

## Fonctionnalités

- Déplacement du serpent avec les touches directionnelles
- Croissance du serpent lorsqu'il mange une pomme
- Système de score
- Menu principal et écran de game over
- Sauvegarde des meilleurs scores

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/Kerlann/python-snake-game.git

# Se déplacer dans le répertoire du projet
cd python-snake-game

# Installer les dépendances
pip install -r requirements.txt

# Lancer le jeu
python main.py
```

## Structure du projet

```
python-snake-game/
│
├── assets/           # Ressources graphiques et sonores
├── src/              # Code source du jeu
│   ├── game/         # Logique du jeu
│   ├── ui/           # Interface utilisateur
│   └── utils/        # Fonctions utilitaires
├── main.py           # Point d'entrée du programme
├── requirements.txt  # Dépendances du projet
└── README.md         # Documentation
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.
