import os
import cv2
import numpy as np
from PIL import Image

def load_single_image(path):
    image = Image.open(path).convert('L')  # Convert to grayscale
    image_array = np.array(image)
    return image_array

def load_images(directory, num_images=1):
    images = []
    count = 0
    for filename in os.listdir(directory):
        if filename.endswith((".png", ".jpg", ".jpeg", ".bmp", ".webp")):
            img = cv2.imread(os.path.join(directory, filename))
            if img is not None:
                images.append((directory, img))
                count += 1
    return images
