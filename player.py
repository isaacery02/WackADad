# player.py

import pygame
from settings import WIDTH, HEIGHT, BLUE

class Player:
    """Represents the player's arrow gun."""

    def __init__(self):
        self.width = 60
        self.height = 60
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 80  # Adjusted position for arrow
        self.speed = 6

    def move(self, keys):
        """Moves the gun left and right based on key presses."""
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

    def draw(self, screen):
        """Draws an arrow instead of a rectangle."""
        points = [
            (self.x + self.width // 2, self.y),  # Top point of the arrow
            (self.x, self.y + self.height),  # Bottom-left
            (self.x + self.width, self.y + self.height)  # Bottom-right
        ]
        pygame.draw.polygon(screen, BLUE, points)  # Draw the arrow
