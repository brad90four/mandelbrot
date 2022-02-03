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
# interesting points:
# x=-0.7756837699949401 y=-0.13646736999704
# x= 0.001643721971153 y =-0.822467633298876

def point_test(x, y, zoom, test_num):
    plt.imshow(
        mandelbrot(
            height=1024,
            width=1024,
            x=x,
            y=y,
            zoom=zoom,
            max_iterations=1000
        ),
        cmap="gist_ncar"
    )
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.savefig(f"image_test_{test_num}.jpg", dpi=300, bbox_inches="tight", pad_inches=0, transparent=True)
    print(f"{x = }, {y = }")



def pallete_test():
    palletes = [
        'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot',
        'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
        'turbo', 'nipy_spectral', 'gist_ncar'
    ]
    zoom = 10000
    iteration = 100
    for pallete in palletes:
        plt.imshow(
            mandelbrot(
                height=1024,
                width=1024,
                x=0.001643721971153,
                y=-0.822467633298876,
                zoom=zoom,
                max_iterations=iteration
            ),
            cmap=pallete
        )
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        plt.savefig(f"image_{pallete}.jpg", dpi=300, bbox_inches="tight", pad_inches=0, transparent=True)
        print(f"{pallete}")



def anim_image():
    for i in range(0, 51):
        if i == 1:
            zoom = 1
        else:
            zoom = int(10 ** (0.25 * i)) # every 4 iterations, zoom 10x

        iteration = 100 * int(max(1, np.floor(np.log10(zoom))))

        plt.imshow(
            mandelbrot(
                height=1024,
                width=1024,
                x=-0.7756837699949401,
                y=-0.13646736999704,
                zoom=zoom,
                max_iterations=iteration
            ),
            cmap="gist_ncar"
        )
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        plt.savefig(f"image_{i}.jpg", dpi=300, bbox_inches="tight", pad_inches=0, transparent=True)
        print(f"{i}: {zoom = }, {iteration = }")



def param_tester():
    # optimal: dpi 300, size 1024, iteration 100-1000
    #dpis = [100, 300, 500]
    sizes = [(512, 512), (1024, 1024), (2048, 2048)]
    iterations = [100, 500, 1000, 5000]
    zooms = [1, 100, 1000, 10000]

    for size in sizes:
        dpi = 300
        for iteration in iterations:
            for zoom in zooms:
                    plt.imshow(
                        mandelbrot(
                            height=size[0],
                            width=size[1],
                            x=0.001643721971153,
                            y=-0.822467633298876,
                            zoom=zoom,
                            max_iterations=iteration
                        ),
                        cmap="nipy_spectral"
                    )
                    ax = plt.gca()
                    ax.axes.xaxis.set_visible(False)
                    ax.axes.yaxis.set_visible(False)
                    plt.savefig(f"image_{dpi}_{zoom}_{size[0]}_{iteration}.jpg", dpi=dpi, bbox_inches="tight", pad_inches=0, transparent=True)
                    print(f"{dpi = }, {zoom= }, {size[0] = }, {iteration = }")


# center of spiral: -0.77568377 + 0.13646737j
# neck: -e/7 - e/20j
# some other: 0.25 + 0j
# lightning: -0.170337 -1.06506j
# jigsaw: 0.42884 -0.231345j
# sticks: -1.62917 -0.0203968j
# other spiral : -0.761574 -0.0847596j
# seahorse: -0.75 + 0.05j
# elephant: 0.1 + 0.1j

### awesome sauce
# wiki: 0.001643721971153 − 0.822467633298876i

# big zoom real: -1.77983107263358987710609737625462554160612202082973721464269536941106123136243079619230058357360213932827
# big zoom imag: 0.0000768808104690890642867866831207682698968739265086118371576831945033925898525759232427462136212757994983490243570012245

# julias
# -0.79 + 0.15j
# -0.162 + 1.04j
# 0.3 - 0.1j
# -1.476 + 0j
# 0.28 + 0.008j


# point_test(x=-0.7756837699949401, y=-0.13646736999704, zoom=1000000000000000, test_num=11)
# pallete_test()
# param_tester()
anim_image()