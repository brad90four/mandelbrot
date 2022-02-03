from PIL import Image
import os
from pathlib import Path


image_list = sorted(os.listdir(Path(__file__).parent), key=os.path.getmtime)
reversed_images = image_list[::-1]
all_images = image_list + reversed_images

images = [Image.open(file) for file in all_images if ".jpg" in file]

images[0].save(
    "mandelbrot.gif",
    save_all=True,
    append_images=images,
    optimize=True,
    duration=200,
    loop=0
)
