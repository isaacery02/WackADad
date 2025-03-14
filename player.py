# player.py

import pygame
from settings import WIDTH, HEIGHT

class Player:
    """Represents the player's gun."""
    
    def __init__(self):
        self.width = 60
        self.height = 30
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 60
        self.speed = 5

    def move(self, keys):
        """Moves the gun left and right."""
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

    def draw(self, screen):
        """Draws the gun."""
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
