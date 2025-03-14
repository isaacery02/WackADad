# powerups.py

import pygame
import random
from settings import WIDTH, HEIGHT

# Load power-up image (lightning bolt)
powerup_img = pygame.image.load("Images/powerup.png")
powerup_img = pygame.transform.scale(powerup_img, (40, 40))

class PowerUp:
    """Represents a moving power-up that increases bullet speed."""
    
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT // 2)
        self.speed_x = random.choice([-4, 4])  # Moves faster than the head
        self.speed_y = random.choice([-4, 4])
        self.width = 40
        self.height = 40

    def move(self):
        """Moves the power-up, bouncing off walls."""
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off walls
        if self.x <= 0 or self.x >= WIDTH - self.width:
            self.speed_x = -self.speed_x
        if self.y <= 0 or self.y >= HEIGHT - self.height:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        """Draws the power-up."""
        screen.blit(powerup_img, (self.x, self.y))
