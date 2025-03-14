# head.py

import cv2
import pygame
import random
import os
from settings import WIDTH, HEIGHT

# Create Images folder if not exists
if not os.path.exists("Images"):
    os.makedirs("Images")

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
            cv2.imwrite(image_path, frame)  # Save without rotation
            break
        elif key == 27:  # ESC key to cancel
            cam.release()
            cv2.destroyAllWindows()
            exit()

    cam.release()
    cv2.destroyAllWindows()
    return image_path

class Head:
    """Represents the bouncing head target."""
    
    def __init__(self):
        image_path = capture_photo()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(100, HEIGHT // 2)  # Start in the upper half
        self.speed_x = random.choice([-3, 3])
        self.speed_y = random.choice([-3, 3])

    def move(self):
        """Moves the head and bounces off walls."""
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off walls
        if self.x <= 0 or self.x >= WIDTH - 80:
            self.speed_x = -self.speed_x
        if self.y <= 0 or self.y >= HEIGHT // 2:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        """Draws the head."""
        screen.blit(self.image, (self.x, self.y))
