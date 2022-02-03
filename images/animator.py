import os
from pathlib import Path

import cv2

image_list = sorted(os.listdir(Path(__file__).parent), key=os.path.getmtime)
reversed_images = image_list[::-1]
all_images = image_list + reversed_images
all_images = [image for image in all_images if "jpg" in image]

images = [cv2.imread(image) for image in all_images]
width, height, c = cv2.imread(all_images[0]).shape
out = cv2.VideoWriter(
    "mandelbrot.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 5, (width, height)
)
for image in images:
    out.write(image)
out.release()
