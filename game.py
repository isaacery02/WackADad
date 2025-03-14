# game.py

import pygame
import random
import time
from settings import *
from head import Head
from player import Player
from bullet import Bullet
from obstacles import Obstacle

# Initialize pygame display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load sound effects
gunshot_sound = pygame.mixer.Sound("Audio/gunshot.wav")
pop_sound = pygame.mixer.Sound("Audio/pop.wav")

def run_game():
    """Main game function."""
    player = Player()
    head = Head()  # Capture and use the new webcam photo
    obstacles = [Obstacle() for _ in range(3)]
    bullets = []
    score = 0

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Event handling
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.x, player.y))
                gunshot_sound.play()

        # Move entities
        player.move(keys)
        head.move()
        for bullet in bullets:
            bullet.move()

        # Remove off-screen bullets
        bullets = [b for b in bullets if not b.off_screen()]

        # Check bullet collisions with obstacles
        for obstacle in obstacles:
            bullets = [b for b in bullets if not (
                obstacle.x < b.x < obstacle.x + obstacle.width and
                obstacle.y < b.y < obstacle.y + obstacle.height
            )]

        # Check bullet collision with head
        for bullet in bullets:
            if head.x < bullet.x < head.x + 80 and head.y < bullet.y < head.y + 80:
                bullets.remove(bullet)
                pop_sound.play()
                score += 1
                head = Head()  # Capture a new photo for the head

        # Draw everything
        player.draw(screen)
        head.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
        pygame.display.flip()
        clock.tick(60)

run_game()
