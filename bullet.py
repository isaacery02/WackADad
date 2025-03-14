# bullet.py

import pygame
from settings import HEIGHT

class Bullet:
    """Represents a bullet fired by the player."""
    
    def __init__(self, x, y, speed):
        self.x = x + 25  # Centered from the gun
        self.y = y
        self.speed = speed  # Dynamic speed based on power-up
        self.radius = 5

    def move(self):
        """Moves the bullet upward."""
        self.y += self.speed

    def draw(self, screen):
        """Draws the bullet."""
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

    def off_screen(self):
        """Checks if the bullet is off-screen."""
        return self.y < 0
