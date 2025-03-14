# obstacles.py

import pygame
import random
from settings import WIDTH, HEIGHT

class Obstacle:
    """Represents a round obstacle that moves slowly and blocks bullets."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(20, 50)
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )  # Random colors
        self.speed_x = random.choice([-1, 0, 1])  # Slow movement speed
        self.speed_y = random.choice([-1, 0, 1])

    def move(self):
        """Moves the obstacle slowly and bounces off walls."""
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off walls
        if self.x <= 0 or self.x >= WIDTH - self.radius:
            self.speed_x = -self.speed_x
        if self.y <= 0 or self.y >= HEIGHT - self.radius:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        """Draws the round obstacle."""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def check_collision(self, bullet):
        """Checks if a bullet hits the obstacle."""
        distance = ((bullet.x - self.x) ** 2 + (bullet.y - self.y) ** 2) ** 0.5
        return distance < self.radius + bullet.radius  # Collides if distance is small

def generate_obstacles(num_obstacles):
    """Evenly spread obstacles across the screen using a grid-based approach."""
    obstacles = []
    grid_size = WIDTH // (num_obstacles // 2)  # Divide width into sections
    y_positions = [HEIGHT // 4, HEIGHT // 2, HEIGHT * 3 // 4]  # Three levels of obstacles

    for i in range(num_obstacles):
        x = (i % (num_obstacles // 2)) * grid_size + grid_size // 2  # Spread evenly
        y = random.choice(y_positions)  # Randomly assign y level

        obstacles.append(Obstacle(x, y))

    return obstacles
