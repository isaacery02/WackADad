# head.py

import cv2
import pygame
import os

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

def load_photo():
    """Loads the captured head image into pygame."""
    image_path = capture_photo()
    head_img = pygame.image.load(image_path)
    head_img = pygame.transform.scale(head_img, (100, 100))
    return head_img
