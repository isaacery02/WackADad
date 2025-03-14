# powerups.py

import pygame
import random
from settings import WIDTH, HEIGHT

# Load power-up image
powerup_img = pygame.image.load("Images/powerup.png")
powerup_img = pygame.transform.scale(powerup_img, (40, 40))

def generate_powerups(obstacles, num_powerups=2):
    """Generates power-ups that don't overlap obstacles."""
    power_ups = []
    while len(power_ups) < num_powerups:
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)

        too_close = any(
            ((x - obs["x"]) ** 2 + (y - obs["y"]) ** 2) ** 0.5 < 50
            for obs in obstacles
        )

        if not too_close:
            power_ups.append({"x": x, "y": y})

    return power_ups

def draw_powerups(screen, power_ups):
    """Draws power-ups on the screen."""
    for power in power_ups:
        screen.blit(powerup_img, (power["x"] - 20, power["y"] - 20))
