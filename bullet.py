# bullet.py

import pygame
from settings import HEIGHT, RED

class Bullet:
    """Represents a bullet fired by the player."""
    
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = 5  # Define bullet size

    def move(self):
        """Moves the bullet upward."""
        self.y += self.speed

    def draw(self, screen):
        """Draws the bullet."""
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

    def off_screen(self):
        """Checks if the bullet is off-screen."""
        return self.y < 0

    def check_collision(self, obj):
        """Checks if the bullet collides with an object (obstacle, power-up, or head)."""
        if not hasattr(obj, "radius"):  # Ensure obj has a radius attribute
            return False
        distance = ((self.x - (obj.x + obj.radius)) ** 2 + (self.y - (obj.y + obj.radius)) ** 2) ** 0.5
        return distance < self.radius + obj.radius
