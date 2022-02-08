import os
from tkinter import Tk, filedialog

from PIL import Image

import cv2

root = Tk()
image_folder = filedialog.askdirectory(
    initialdir="/", title="Please select a directory"
)
root.destroy()


image_list = sorted(os.listdir(image_folder, key=os.path.getctime))
reversed_images = image_list[::-1]
all_images = image_list + reversed_images
all_images = [image for image in all_images if "png" in image]


def mp4(save_name, fps):
    save_name = save_name
    images = [cv2.imread(image) for image in all_images]
    width, height, c = cv2.imread(all_images[0]).shape
    out = cv2.VideoWriter(
        f"{save_name}.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )
    for image in images:
        out.write(image)
    out.release()


def gif(save_name):
    images = [Image.open(file) for file in all_images if ".png" in file]
    images[0].save(
        f"{save_name}.gif",
        save_all=True,
        append_images=images,
        optimize=True,
        # duration=200,
        loop=0,
    )


if __name__ == "__main__":
    # gif("julia_test")
    mp4("circle1", 10)
