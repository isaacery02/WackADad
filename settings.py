# settings.py

import pygame

# Screen settings
WIDTH, HEIGHT = 500, 700  # Taller screen for shooting

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GRAY = (150, 150, 150)

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 48)
