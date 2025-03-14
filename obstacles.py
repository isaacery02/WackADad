# obstacles.py

import pygame
import random
from settings import WIDTH, HEIGHT

class Obstacle:
    """Represents an obstacle that blocks bullets."""
    
    def __init__(self):
        self.x = random.randint(50, WIDTH - 100)
        self.y = random.randint(HEIGHT // 3, HEIGHT // 2)
        self.width = random.randint(30, 80)
        self.height = 20
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )  # Random colors

    def draw(self, screen):
        """Draws the obstacle."""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
