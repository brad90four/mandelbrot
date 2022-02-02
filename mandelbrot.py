from dataclasses import dataclass
import matplotlib.cm
import numpy as np
from PIL import Image
from math import log, e

np.warnings.filterwarnings("ignore")


@dataclass
class Viewport:
    image: Image.Image
    center: complex
    width: float

    @property
    def height(self):
        return self.scale * self.image.height

    @property
    def offset(self):
        return self.center + complex(-self.width, self.height) / 2

    @property
    def scale(self):
        return self.width / self.image.width

    def __iter__(self):
        for y in range(self.image.height):
            for x in range(self.image.width):
                yield Pixel(self, x, y)


@dataclass
class Pixel:
    viewport: Viewport
    x: int
    y: int

    @property
    def color(self):
        return self.viewport.image.getpixel((self.x, self.y))

    @color.setter
    def color(self, value):
        self.viewport.image.putpixel((self.x, self.y), value)

    def __complex__(self):
        return complex(self.x, -self.y) * self.viewport.scale + self.viewport.offset


@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius: float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def stability(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.escape_count(c, smooth) / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def escape_count(self, c: complex, smooth=False) -> int | float:
        z = 0
        for iteration in range(self.max_iterations):
            z = z**2 + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iteration + 1 - log(log(abs(z))) / log(2)
                return iteration
        return self.max_iterations


def paint(mandelbrot_set, viewport, palette, smooth):
    for pixel in viewport:
        stability = mandelbrot_set.stability(complex(pixel), smooth=True)
        # index = int(min(stability * len(palette), len(palette) - 1))
        # pixel.color = palette[index % len(palette)]
        colors = [c for c in palette(stability)[0:-1]]
        # colors.append(colors.pop(0))
        # colors.append(colors.pop(1))
        pixel.color = tuple([(int(color * 255)) for color in colors])
        # pixel.color = tuple([(int((1 - color) * 255)) for color in colors])


# def denormalize(palette):
#     return [tuple(int(channel * 255) for channel in color) for color in palette]
# colormap = matplotlib.cm.get_cmap("twilight").colors
# palette = denormalize(colormap)
# palette = matplotlib.cm.get_cmap("jet")
# mandelbrot_set = MandelbrotSet(max_iterations=500, escape_radius=1000)
# image = Image.new(mode="RGB", size=(512, 512))
# viewport = Viewport(image, center=-0.74339 + 0.13129j, width=1/10)
# paint(mandelbrot_set, viewport, palette, smooth=True)
# image.show()

# palletes = [
#     'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot',
#     'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
#     'turbo', 'nipy_spectral', 'gist_ncar'
# ]

# for p in palletes:
#     palette = matplotlib.cm.get_cmap(p)
#     mandelbrot_set = MandelbrotSet(max_iterations=100, escape_radius=1000)
#     image = Image.new(mode="RGB", size=(512, 512))
#     viewport = Viewport(image, center=-0.74339 + 0.13129j, width=1/10)
#     paint(mandelbrot_set, viewport, palette, smooth=True)
#     image.save(f"image_{p}.jpg")


palette = matplotlib.cm.get_cmap("rainbow")
start_width = 2.5
start_iter = 500
for i in range(101):
    if i == 0:
        width = start_width
        mandelbrot_set = MandelbrotSet(max_iterations=start_iter, escape_radius=1000)
    else:
        width = start_width / (10 ** (0.5 * i))
        mandelbrot_set = MandelbrotSet(max_iterations=int(start_iter * 1.25 ** i), escape_radius=1000)
    image = Image.new(mode="RGB", size=(512, 512))
    viewport = Viewport(image, center=-0.77568377 + 0.13646737j, width=width)
    paint(mandelbrot_set, viewport, palette, smooth=True)
    image.save(f"image_{i}.jpg")
    print(f"Finished image: {i}. Width: {width}, iter: {int(start_iter * 1.25 ** i)}")


def test_center(zoom, c):
    palette = matplotlib.cm.get_cmap("nipy_spectral")
    mandelbrot_set = MandelbrotSet(max_iterations=1000, escape_radius=1000)
    image = Image.new(mode="RGB", size=(512, 512))
    viewport = Viewport(image, center=c, width=1 / zoom)
    paint(mandelbrot_set, viewport, palette, smooth=True)
    image.save(f"test_{c}_zoom{zoom}.jpg")
    print(f"{zoom = }, {c = }")


# test_point = (-0.77568377 + 0.13646737j)
# test_center(10000000, test_point)

# center of spiral: -0.77568377 + 0.13646737j
# neck: -e/7 - e/20j
# some other: 0.25 + 0j
# lightning: -0.170337 -1.06506j
# jigsaw: 0.42884 -0.231345j
# sticks: -1.62917 -0.0203968j
# other spiral : -0.761574 -0.0847596j
# seahorse: -0.75 + 0.1j
# elephant: 0.1 + 0.1j

