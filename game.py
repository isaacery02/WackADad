import pygame

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball settings
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_radius = 20
ball_speed = [3, 3]

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Move the ball
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Bounce off walls
    if ball_pos[0] - ball_radius <= 0 or ball_pos[0] + ball_radius >= WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball_pos[1] - ball_radius <= 0 or ball_pos[1] + ball_radius >= HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Draw the ball
    pygame.draw.circle(screen, RED, ball_pos, ball_radius)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()
