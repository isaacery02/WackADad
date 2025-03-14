import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pop Isaac's Head!")

# Load and rotate head image
head_img = pygame.image.load("Images/head.png")
head_img = pygame.transform.scale(head_img, (100, 100))
head_img = pygame.transform.rotate(head_img, 90)  # Rotate 90 degrees RIGHT

# Load sound effect
pop_sound = pygame.mixer.Sound("Audio/pop.wav")

# Game variables
size = 100  # Initial size of the head
speed_x = random.choice([-3, 3])
speed_y = random.choice([-3, 3])
score = 0

# Timer setup (1-minute game)
start_time = time.time()
game_duration = 60  # 60 seconds

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 48)


# Function to check if a new position collides with obstacles
def is_colliding_with_obstacles(x, y, size, obstacles):
    for obstacle in obstacles:
        distance = ((x + size // 2 - obstacle["x"]) ** 2 + (y + size // 2 - obstacle["y"]) ** 2) ** 0.5
        if distance < (size // 2 + obstacle["radius"] + 10):  # Add buffer space
            return True
    return False


# Function to generate non-overlapping obstacles
def generate_obstacles(num_obstacles, min_distance=70):
    obstacles = []
    while len(obstacles) < num_obstacles:
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        radius = random.randint(20, 40)
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

        # Ensure obstacles don't overlap
        too_close = False
        for obs in obstacles:
            distance = ((x - obs["x"]) ** 2 + (y - obs["y"]) ** 2) ** 0.5
            if distance < radius + obs["radius"] + min_distance:
                too_close = True
                break

        if not too_close:
            obstacles.append({"x": x, "y": y, "radius": radius, "color": color})

    return obstacles


# Generate obstacles
obstacles = generate_obstacles(5)

# Ensure the head does NOT spawn inside an obstacle
while True:
    head_x = random.randint(100, WIDTH - 100)
    head_y = random.randint(100, HEIGHT - 100)
    if not is_colliding_with_obstacles(head_x, head_y, size, obstacles):
        break  # Found a valid position

# Clock
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((255, 255, 255))  # White background

    # Time remaining
    elapsed_time = time.time() - start_time
    time_left = max(0, int(game_duration - elapsed_time))

    # Move the head
    new_x, new_y = head_x + speed_x, head_y + speed_y

    # Bounce off walls
    if new_x <= 0 or new_x >= WIDTH - size:
        speed_x = -speed_x
    if new_y <= 0 or new_y >= HEIGHT - size:
        speed_y = -speed_y

    # Check collision with obstacles
    head_center = (new_x + size // 2, new_y + size // 2)
    for obstacle in obstacles:
        distance = ((head_center[0] - obstacle["x"]) ** 2 + (head_center[1] - obstacle["y"]) ** 2) ** 0.5
        if distance < size // 2 + obstacle["radius"] + 5:  # Buffer to prevent sticking
            speed_x = -speed_x
            speed_y = -speed_y
            head_x += speed_x * 5  # Move away to avoid getting stuck
            head_y += speed_y * 5
            break  # Stop checking other obstacles

    # Update position
    head_x += speed_x
    head_y += speed_y

    # Draw head
    resized_head = pygame.transform.scale(head_img, (size, size))
    screen.blit(resized_head, (head_x, head_y))

    # Draw obstacles (smooth anti-aliased circles)
    for obstacle in obstacles:
        pygame.draw.circle(screen, obstacle["color"], (obstacle["x"], obstacle["y"]), obstacle["radius"])

    # Draw score and timer
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    timer_text = font.render(f"Time: {time_left}s", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(timer_text, (WIDTH - 120, 10))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:  # Detect tap/click
            mx, my = pygame.mouse.get_pos()
            if head_x < mx < head_x + size and head_y < my < head_y + size:
                pop_sound.play()  # Play pop sound
                score += 1  # Increase score
                size = max(30, size - 5)  # Shrink the head after each pop

                # Find a new valid spawn position
                while True:
                    head_x = random.randint(100, WIDTH - 100)
                    head_y = random.randint(100, HEIGHT - 100)
                    if not is_colliding_with_obstacles(head_x, head_y, size, obstacles):
                        break  # Found a valid position

                # Random new movement direction
                speed_x = random.choice([-3, 3])
                speed_y = random.choice([-3, 3])

    # Check if time is up
    if time_left <= 0:
        screen.fill((255, 255, 255))
        game_over_text = big_font.render("Game Over!", True, (255, 0, 0))
        final_score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 40))
        screen.blit(final_score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 10))
        pygame.display.flip()
        pygame.time.delay(3000)  # Show for 3 seconds
        running = False

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()
