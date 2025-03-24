# Jeu Snake en Python

Un jeu Snake classique développé en Python avec la bibliothèque Pygame.

![Capture d'écran du jeu](docs/screenshots/screenshot.png)

## Description

Ce projet est une implémentation du jeu classique Snake où le joueur contrôle un serpent qui grandit en mangeant des pommes. Le jeu se termine lorsque le serpent se heurte à lui-même ou aux murs.

## Fonctionnalités

- Déplacement du serpent avec les touches directionnelles
- Différents types de nourriture avec des effets spéciaux
  - Pomme rouge : points standard
  - Pomme dorée : bonus de points
  - Pomme bleue : augmente temporairement la vitesse
  - Pomme verte : réduit temporairement la vitesse
- Système de score et sauvegarde des meilleurs scores
- Menu principal interactif
- Écran de game over
- Système de niveaux avec augmentation progressive de la difficulté
- Obstacles qui apparaissent à partir du niveau 3
- Sons et musique avec options de configuration
- Mode débogage pour les développeurs

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

## Utilisation

### Contrôles du jeu

- **Flèches directionnelles** : Déplacer le serpent
- **P** : Mettre en pause / Reprendre le jeu
- **Échap** : Retourner au menu / Quitter

### Options en ligne de commande

Le jeu prend en charge les options suivantes en ligne de commande :

```bash
# Lancer le jeu en mode débogage
python main.py --debug

# Exécuter les tests unitaires
python main.py --test
```

## Personnalisation

### Musique et sons

Vous pouvez personnaliser les sons et la musique du jeu en remplaçant les fichiers dans les dossiers suivants :

- `assets/sounds/` : Contient les effets sonores
- `assets/music/` : Contient les fichiers de musique

Consultez les fichiers README.md dans ces dossiers pour plus d'informations sur les formats et les noms de fichiers attendus.

### Niveaux et difficulté

Vous pouvez modifier les paramètres de difficulté en éditant le fichier `src/utils/constants.py` :

```python
# Paramètres du jeu
FPS = 60
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10  # cases par seconde
```

## Structure du projet

```
python-snake-game/
│
├── assets/             # Ressources graphiques et sonores
│   ├── music/         # Fichiers musicaux
│   └── sounds/        # Effets sonores
│
├── logs/               # Journaux de débogage
│
├── src/                # Code source du jeu
│   ├── game/          # Logique du jeu
│   │   ├── food.py    # Gestion de la nourriture
│   │   ├── game.py    # Classe principale du jeu
│   │   ├── level.py   # Système de niveaux
│   │   ├── score.py   # Système de score
│   │   └── snake.py   # Gestion du serpent
│   │
│   ├── ui/            # Interface utilisateur
│   │   ├── game_over.py      # Écran de fin de partie
│   │   ├── highscore_screen.py # Écran des meilleurs scores
│   │   ├── menu.py           # Menu principal
│   │   └── sound_options.py  # Options sonores
│   │
│   └── utils/         # Fonctions utilitaires
│       ├── constants.py      # Constantes du jeu
│       ├── highscore.py      # Gestion des meilleurs scores
│       ├── logger.py         # Système de journalisation
│       └── sound_manager.py  # Gestion des sons et de la musique
│
├── tests/              # Tests unitaires
│   ├── test_food.py          # Tests pour la classe Food
│   ├── test_score.py         # Tests pour la classe Score
│   ├── test_snake.py         # Tests pour la classe Snake
│   ├── performance_test.py   # Tests de performance
│   └── run_tests.py          # Script pour exécuter tous les tests
│
├── main.py             # Point d'entrée du programme
├── requirements.txt    # Dépendances du projet
└── README.md           # Documentation
```

## Développement

### Tests

Pour exécuter les tests unitaires :

```bash
python main.py --test
```

Ou directement :

```bash
python -m tests.run_tests
```

Pour exécuter les tests de performance :

```bash
python -m tests.performance_test
```

### Débogage

Pour lancer le jeu en mode débogage :

```bash
python main.py --debug
```

Ce mode affiche des informations supplémentaires sur l'écran et génère des logs détaillés dans le dossier `logs/`.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

### Processus de contribution

1. Forkez le dépôt
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.

## Auteurs

- [Kerlann](https://github.com/Kerlann)

## Remerciements

- Pygame pour la bibliothèque de jeu
- [OpenGameArt](https://opengameart.org/) pour l'inspiration des sons et graphismes
