# powerups.py

import pygame
import random
from settings import WIDTH, HEIGHT

# Load power-up image
powerup_img = pygame.image.load("Images/powerup.png")
powerup_img = pygame.transform.scale(powerup_img, (40, 40))

class PowerUp:
    """Represents a moving power-up."""
    
    def __init__(self, obstacles):
        while True:
            self.x = random.randint(50, WIDTH - 50)
            self.y = random.randint(50, HEIGHT - 50)
            self.radius = 20
            self.speed_x = random.choice([-4, 4])  # Moves faster than the head
            self.speed_y = random.choice([-4, 4])

            # Ensure power-up doesn't spawn inside an obstacle
            if not any(
                ((self.x - obs["x"]) ** 2 + (self.y - obs["y"]) ** 2) ** 0.5 < self.radius + obs["radius"] + 10
                for obs in obstacles
            ):
                break  # Found a valid position
    
    def move(self, obstacles):
        """Moves the power-up, bouncing off walls & obstacles."""
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off walls
        if self.x <= 0 or self.x >= WIDTH - self.radius:
            self.speed_x = -self.speed_x
        if self.y <= 0 or self.y >= HEIGHT - self.radius:
            self.speed_y = -self.speed_y

        # Bounce off obstacles
        for obstacle in obstacles:
            distance = ((self.x - obstacle["x"]) ** 2 + (self.y - obstacle["y"]) ** 2) ** 0.5
            if distance < self.radius + obstacle["radius"]:
                self.speed_x = -self.speed_x
                self.speed_y = -self.speed_y
                break  # Prevent multiple bounces in one frame

    def draw(self, screen):
        """Draws the power-up on screen."""
        screen.blit(powerup_img, (self.x - self.radius, self.y - self.radius))
