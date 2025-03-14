import pygame
import random
import time
import cv2
from settings import *
from head import Head
from player import Player
from bullet import Bullet
from obstacles import generate_obstacles
from powerups import PowerUp

# Initialize pygame display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load sound effects
gunshot_sound = pygame.mixer.Sound("Audio/gunshot.wav")
pop_sound = pygame.mixer.Sound("Audio/pop.wav")

# Capture the image ONCE and use it for the entire game
def capture_photo():
    """Captures a photo using the webcam and saves it."""
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Take a Picture (Press SPACE to capture)")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture image.")
            break

        cv2.imshow("Take a Picture (Press SPACE to capture)", frame)

        key = cv2.waitKey(1)
        if key == 32:  # SPACE key to capture
            image_path = "Images/captured_head.png"
            cv2.imwrite(image_path, frame)
            break
        elif key == 27:  # ESC key to cancel
            cam.release()
            cv2.destroyAllWindows()
            exit()

    cam.release()
    cv2.destroyAllWindows()
    return pygame.image.load(image_path)

def game_over_screen(score):
    """Displays the Game Over screen with a retry button."""
    screen.fill(WHITE)

    # Display Game Over text
    game_over_text = font.render("Game Over!", True, BLACK)
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    retry_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 40, 100, 40)  # Retry button

    # Center the text
    screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))

    # Draw retry button
    pygame.draw.rect(screen, GREEN, retry_button)
    pygame.draw.rect(screen, BLACK, retry_button, 2)  # Border
    screen.blit(font.render("Retry", True, WHITE), (WIDTH // 2 - 25, HEIGHT // 2 + 50))

    pygame.display.flip()

    # Wait for user to click Retry or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if retry_button.collidepoint(mx, my):
                    run_game()  # Restart the game

def run_game():
    """Main game function."""
    player = Player()
    obstacles = generate_obstacles(6)  # Evenly spread obstacles
    head_img = capture_photo()  # Take photo ONCE
    head = Head(head_img, obstacles)  # Use the captured image
    powerups = [PowerUp() for _ in range(2)]  # Power-ups
    bullets = []
    score = 0
    bullet_speed = -5  # Bullet speed
    game_duration = 5 # Game time in seconds
    start_time = time.time()

    # Define exit button
    exit_button = pygame.Rect(WIDTH - 60, 10, 50, 30)

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Calculate remaining time
        elapsed_time = time.time() - start_time
        time_left = max(0, int(game_duration - elapsed_time))

        # Stop the game when the timer reaches 0
        if time_left <= 0:
            game_over_screen(score)
            return  # Stop the game

        # Event handling
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if exit_button.collidepoint(mx, my):
                    running = False  # Quit the game

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.x + player.width // 2 - 5, player.y, bullet_speed))  # Bullet fires from tip
                gunshot_sound.play()

        # Move player
        player.move(keys)

        # Move obstacles slowly
        for obstacle in obstacles:
            obstacle.move()

        # Move head and other entities
        head.move(obstacles)
        for powerup in powerups:
            powerup.move()
        for bullet in bullets:
            bullet.move()

        # Remove off-screen bullets
        bullets = [b for b in bullets if not b.off_screen()]

        # Check bullet collisions with obstacles
        for bullet in bullets[:]:  
            for obstacle in obstacles:
                if bullet.check_collision(obstacle):
                    bullets.remove(bullet)  

        # Check bullet collision with power-ups
        for bullet in bullets[:]:  
            for powerup in powerups[:]:
                if bullet.check_collision(powerup):
                    bullets.remove(bullet)
                    powerups.remove(powerup)
                    bullet_speed = -7  # Speed up bullets

        # Check bullet collision with head
        for bullet in bullets[:]:  
            if bullet.check_collision(head):
                bullets.remove(bullet)
                pop_sound.play()
                score += 1
                head.x, head.y = head.find_safe_spawn(obstacles)  # Move head to a new safe position

        # Draw everything
        player.draw(screen)
        head.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)

        # 🎯 **Draw UI Elements (Final Placement)**
        # Draw total score (left)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (20, 10))  # Positioned on the left

        # Draw timer (centered)
        timer_text = font.render(f"Time: {time_left}s", True, BLACK)
        screen.blit(timer_text, (WIDTH // 2 - 40, 10))  # Positioned in the middle

        # Draw exit button (right)
        pygame.draw.rect(screen, RED, exit_button)
        pygame.draw.rect(screen, BLACK, exit_button, 2)  # Border
        screen.blit(font.render("X", True, WHITE), (WIDTH - 55, 15))

        pygame.display.flip()
        clock.tick(30)

run_game()
