import numpy as np
import matplotlib.pyplot as plt


def mandelbrot(height, width, x=-0.5, y=0, zoom=1, max_iterations=100):
    # To make navigation easier we calculate these values
    x_width = 1.5
    y_height = 1.5*height/width
    x_from = x - x_width/zoom
    x_to = x + x_width/zoom
    y_from = y - y_height/zoom
    y_to = y + y_height/zoom
    # Here the actual algorithm starts
    x = np.linspace(x_from, x_to, width).reshape((1, width))
    y = np.linspace(y_from, y_to, height).reshape((height, 1))
    c = x + 1j * y
    # Initialize z to all zero
    z = np.zeros(c.shape, dtype=np.complex128)
    # To keep track in which iteration the point diverged
    div_time = np.zeros(z.shape, dtype=int)
    # To keep track on which points did not converge so far
    m = np.full(c.shape, True, dtype=bool)
    for i in range(max_iterations):
        z[m] = z[m]**2 + c[m]
        diverged = np.greater(np.abs(z), 2, out=np.full(c.shape, False), where=m) # Find diverging
        div_time[diverged] = i      # set the value of the diverged iteration number
        m[np.abs(z) > 2] = False    # to remember which have diverged
    return div_time


# Default image of Mandelbrot set
# plt.imshow(mandelbrot(800, 1000), cmap='magma')
# plt.show()

# plt.imshow(mandelbrot(512, 512, -0.77568377, -0.13646737, 1, 100), cmap="jet")
# plt.show()


for i in range(101):
    if i == 0:
        zoom = 1
    else:
        zoom = int(10 ** (0.25 * i))
    if zoom < 1000 and i != 0:
        iteration = 500
    elif i == 0:
        iteration = 1000
    else:
        iteration = int(100 * 2 * i)
    print(f"{i}: {zoom = }, {iteration = }")
    plt.imshow(
        mandelbrot(
            height=512,
            width=512,
            x=-0.77568377,
            y=-0.13646737,
            zoom=zoom,
            max_iterations=iteration
        ),
        cmap="twilight"
    )
    plt.savefig(f"image_{i}.jpg")

# center of spiral: -0.77568377 + 0.13646737j
# neck: -e/7 - e/20j
# some other: 0.25 + 0j
# lightning: -0.170337 -1.06506j
# jigsaw: 0.42884 -0.231345j
# sticks: -1.62917 -0.0203968j
# other spiral : -0.761574 -0.0847596j
# seahorse: -0.75 + 0.1j
# elephant: 0.1 + 0.1j
