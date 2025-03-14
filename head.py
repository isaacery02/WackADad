# head.py

import pygame
import random
from settings import WIDTH, HEIGHT

class Head:
    """Represents the bouncing head target."""
    
    def __init__(self, head_img, obstacles):
        """Initialize the head with a preloaded image."""
        self.image = pygame.transform.scale(head_img, (80, 80))
        self.radius = 40  # Define hitbox for bullets
        self.x, self.y = self.find_safe_spawn(obstacles)
        self.speed_x = random.choice([-1, 1])  # Slower movement
        self.speed_y = random.choice([-1, 1])

    def find_safe_spawn(self, obstacles):
        """Finds a safe location for the head that does not overlap obstacles."""
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(50, WIDTH - self.radius * 2 - 50)
            y = random.randint(100, HEIGHT // 2 - self.radius * 2 - 50)  # Now avoids top 100px (timer area)

            # Ensure space is free
            too_close = any(
                ((x - obs.x) ** 2 + (y - obs.y) ** 2) ** 0.5 < self.radius + obs.radius + 30
                for obs in obstacles
            )

            if not too_close:
                return x, y  # Found a valid position
        return 100, 150  # Fallback position, below the timer

    def move(self, obstacles):
        """Moves the head and bounces off walls and obstacles."""
        new_x = self.x + self.speed_x
        new_y = self.y + self.speed_y

        # Bounce off walls
        if new_x <= 0 or new_x >= WIDTH - self.radius * 2:
            self.speed_x = -self.speed_x + random.choice([-1, 1])  # Small random boost to escape
        if new_y <= 0 or new_y >= HEIGHT // 2 - self.radius * 2:
            self.speed_y = -self.speed_y + random.choice([-1, 1])

        # Check collision with obstacles
        for obstacle in obstacles:
            distance = ((new_x + self.radius - obstacle.x) ** 2 + (new_y + self.radius - obstacle.y) ** 2) ** 0.5
            if distance < self.radius + obstacle.radius:  # Bounce if it collides
                self.speed_x = -self.speed_x + random.choice([-1, 1])
                self.speed_y = -self.speed_y + random.choice([-1, 1])
                break

        # Update position
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, screen):
        """Draws the head."""
        screen.blit(self.image, (self.x, self.y))
