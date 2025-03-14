# game.py

import pygame
import random
import time
from settings import *
from head import load_photo
from powerups import generate_powerups, draw_powerups

# Load sound effect
pop_sound = pygame.mixer.Sound("Audio/pop.wav")

# Load head image
head_img = load_photo()

def run_game():
    """Main game function."""
    size = 100  # Initial size of the head
    speed_x = random.choice([-2, 2])
    speed_y = random.choice([-2, 2])
    score = 0
    game_duration = 60  # 60 seconds
    start_time = time.time()

    # Generate obstacles
    obstacles = []
    while len(obstacles) < 5:
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        radius = random.randint(20, 40)

        too_close = any(
            ((x - obs["x"]) ** 2 + (y - obs["y"]) ** 2) ** 0.5 < radius + obs["radius"] + 50
            for obs in obstacles
        )

        if not too_close:
            obstacles.append({"x": x, "y": y, "radius": radius})

    # Generate power-ups
    power_ups = generate_powerups(obstacles)

    # Ensure the head does NOT spawn inside obstacles
    head_x, head_y = 0, 0
    while True:
        head_x = random.randint(100, WIDTH - 100)
        head_y = random.randint(100, HEIGHT - 100)
        if not any(
            ((head_x - obs["x"]) ** 2 + (head_y - obs["y"]) ** 2) ** 0.5 < 50
            for obs in obstacles
        ):
            break

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Time remaining
        elapsed_time = time.time() - start_time
        time_left = max(0, int(game_duration - elapsed_time))

        # Move the head
        head_x += speed_x
        head_y += speed_y

        # Bounce off walls
        if head_x <= 0 or head_x >= WIDTH - size:
            speed_x = -speed_x
        if head_y <= 0 or head_y >= HEIGHT - size:
            speed_y = -speed_y

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.circle(screen, BLACK, (obstacle["x"], obstacle["y"]), obstacle["radius"])

        # Draw power-ups
        draw_powerups(screen, power_ups)

        # Draw head
        screen.blit(pygame.transform.scale(head_img, (size, size)), (head_x, head_y))

        # Draw score and timer
        screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
        screen.blit(font.render(f"Time: {time_left}s", True, BLACK), (WIDTH - 120, 10))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Check if clicked on the head
                if head_x < mx < head_x + size and head_y < my < head_y + size:
                    pop_sound.play()
                    score += 1
                    size = max(30, size - 5)

                    # Respawn head
                    head_x, head_y = random.randint(50, WIDTH - 150), random.randint(50, HEIGHT - 150)

                # Check if clicked on a power-up
                for power in power_ups[:]:
                    if (power["x"] - 20 < mx < power["x"] + 20) and (power["y"] - 20 < my < power["y"] + 20):
                        score += 5
                        size = min(100, size + 10)
                        power_ups.remove(power)

        if time_left <= 0:
            running = False

        pygame.display.flip()
        clock.tick(60)

while True:
    run_game()
