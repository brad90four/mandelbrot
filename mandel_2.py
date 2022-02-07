from ctypes.wintypes import VARIANT_BOOL
import matplotlib.pyplot as plt
import numpy as np
import time


def mandelbrot(height, width, x=-0.5, y=0, zoom=1, max_iterations=100):
    x_width = 1.5
    y_height = 1.5 * height / width
    x_from = x - x_width / zoom
    x_to = x + x_width / zoom
    y_from = y - y_height / zoom
    y_to = y + y_height / zoom

    x = np.linspace(x_from, x_to, width).reshape((1, width))
    y = np.linspace(y_from, y_to, height).reshape((height, 1))
    c = x + 1j * y

    z = np.zeros(c.shape, dtype=np.complex128)
    div_time = np.zeros(z.shape, dtype=int)
    m = np.full(c.shape, True, dtype=bool)

    for i in range(max_iterations):
        z[m] = z[m] ** 2 + c[m]
        diverged = np.greater(np.abs(z), 2, out=np.full(c.shape, False), where=m)
        div_time[diverged] = i - np.log2(max(1, np.log2(i if i > 0 else 1)))
        m[np.abs(z) > 2] = False
    return div_time


def julia_set(
    c=-0.4 + 0.6j, height=512, width=512, x=0, y=0, zoom=1, max_iterations=100
):
    x_width = 1.5
    y_height = 1.5 * height / width
    x_from = x - x_width / zoom
    x_to = x + x_width / zoom
    y_from = y - y_height / zoom
    y_to = y + y_height / zoom

    x = np.linspace(x_from, x_to, width).reshape((1, width))
    y = np.linspace(y_from, y_to, height).reshape((height, 1))
    z = x + 1j * y

    c = np.full(z.shape, c, dtype=np.complex128)
    div_time = np.zeros(z.shape, dtype=int)
    m = np.full(c.shape, True, dtype=bool)
    for i in range(max_iterations):
        z[m] = z[m] ** 2 + c[m]
        m[np.abs(z) > 2] = False
        div_time[m] = i - np.log2(max(1, np.log2(i if i > 0 else 1)))
    return div_time


def plotter(array, image_name, cmap="cubehelix", dpi=300):
    plt.imshow(array, cmap)
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.savefig(
        f"{image_name}.png",
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0,
        transparent=True,
    )


def point_test(mode, x=0, y=0, zoom=1, test_num=1, c=None, iterations=500):
    if mode == "m":
        plotter(
            mandelbrot(
                height=512, width=512, x=x, y=y, zoom=zoom, max_iterations=iterations
            ),
            image_name=f"{mode}_{test_num}",
        )
        print("Finished image")
    elif mode == "j":
        if c is None:
            c = input("Enter a complex number to center on: \n(Example: (0.5, -2)  :  ")
            c = complex(
                float(c.split(",")[0].replace("(", "").replace(" ", "")),
                float(c.split(",")[1].replace("(", "").replace(" ", "")),
            )
        plotter(
            julia_set(
                c=c,
                height=512,
                width=512,
                x=x,
                y=y,
                zoom=zoom,
                max_iterations=iterations,
            ),
            image_name=f"{mode}_{test_num}",
        )
        print("Finished image")
    else:
        raise ValueError("Mode must be 'm' or 'j'")


def pallete_test(mode):
    palletes = [
        "magma",
        "flag",
        "prism",
        "ocean",
        "gist_earth",
        "terrain",
        "gist_stern",
        "gnuplot",
        "gnuplot2",
        "CMRmap",
        "cubehelix",
        "brg",
        "gist_rainbow",
        "rainbow",
        "jet",
        "turbo",
        "nipy_spectral",
        "gist_ncar",
        "twilight",
    ]
    # zoom = 3162277660168
    zoom = 1
    iteration = 1000
    for pallete in palletes:
        if mode == "m":
            plotter(
                mandelbrot(
                    height=1080,
                    width=1920,
                    x=-0.7756837699949401,
                    y=-0.13646736999704,
                    zoom=zoom,
                    max_iterations=iteration,
                ),
                image_name=pallete,
                cmap=pallete,
            )
            print(f"Finished image: {pallete}")
        elif mode == "j":
            c = complex(-0.7756837699949401, -0.13646736999704)
            plotter(
                julia_set(
                    c=c, height=1080, width=1920, zoom=zoom, max_iterations=iteration
                ),
                image_name=f"{mode}_{pallete}",
                cmap=pallete,
            )
            print(f"Finished image: {mode}_{pallete}")
        else:
            raise ValueError("Mode must be 'm' or 'j'")


def anim_image(
    mode, zoom_rate=4, zoom_range=50, iteration=500, x=0, y=0, c=None, zoom_scale=False
):
    for i in range(1, zoom_range):
        if i == 1:
            zoom = 1
        else:
            zoom = int(10 ** ((1 / zoom_rate) * i))  # every x iterations, zoom 10x
        iteration = iteration

        if zoom_scale:
            if zoom < 10:
                iteration = 100
            elif zoom < 10000:
                iteration = 500
            elif zoom >= 1000000:
                iteration = 1000
            else:
                iteration = 100 * int(max(1, np.floor(np.log10(zoom))))

        if mode == "m":
            plotter(
                mandelbrot(
                    height=1024,
                    width=1024,
                    x=x,
                    y=y,
                    zoom=zoom,
                    max_iterations=iteration,
                ),
                image_name=f"image_{mode}_{i}",
            )
            print(f"Finished: 'image_{mode}_{i}.png'")
        elif mode == "j":
            if c is None:
                c = input(
                    "Enter a complex number to center on: \n(Example: (0.5, -2)  :  "
                )
                c = complex(
                    float(c.split(",")[0].replace("(", "").replace(" ", "")),
                    float(c.split(",")[1].replace("(", "").replace(" ", "")),
                )
            plotter(
                julia_set(c=c, x=0, y=0, zoom=zoom, max_iterations=iteration),
                image_name=f"image_{mode}_{i}",
            )
            print(f"Finished: 'image_{mode}_{i}.png'")
        else:
            raise ValueError("Mode must be 'm' or 'j'")


def param_tester(mode, x=0, y=0, c=None):
    # optimal: dpi 300, size 1024, iteration 100-1000
    dpis = [100, 300, 500]
    sizes = [(512, 512), (1024, 1024), (2048, 2048)]
    iterations = [100, 500, 1000, 5000]
    zooms = [1, 100, 1000, 10000]

    for size in sizes:
        dpi = 300
        for iteration in iterations:
            for zoom in zooms:
                if mode == "m":
                    plotter(
                        mandelbrot(
                            height=size[0],
                            width=size[1],
                            x=x,
                            y=y,
                            zoom=zoom,
                            max_iterations=iteration,
                        ),
                        image_name=f"{mode}_image_{dpi}_{zoom}_{size[0]}_{iteration}",
                        dpi=dpi,
                    )
                    print(
                        f"Finished: '{mode}_image_{dpi}_{zoom}_{size[0]}_{iteration}.png'"
                    )
                elif mode == "j":
                    if c is None:
                        c = input(
                            "Enter a complex number to center on: \n(Example: (0.5, -2)  :  "
                        )
                        c = complex(
                            float(c.split(",")[0].replace("(", "").replace(" ", "")),
                            float(c.split(",")[1].replace("(", "").replace(" ", "")),
                        )
                    plotter(
                        julia_set(
                            c=c,
                            height=size[0],
                            width=size[1],
                            x=x,
                            y=y,
                            zoom=zoom,
                            max_iterations=iteration,
                        ),
                        image_name=f"{mode}_image_{dpi}_{zoom}_{size[0]}_{iteration}",
                        dpi=dpi,
                    )
                    print(
                        f"Finished: '{mode}_image_{dpi}_{zoom}_{size[0]}_{iteration}.png'"
                    )
                else:
                    raise ValueError("Mode must be 'm' or 'j'")


point_collection = {
    "mandelbrot": [
        (-0.7756837699949401, -0.13646736999704),
        (-0.001643721971153, -0.822467633298876),
        (-0.7746806106269039, -0.1374168856037867),
        (
            -0.9223327810370947027656057193752719757635,
            0.3102598350874576432708737495917724836010,
        ),
        (3162277660168, (-0.7746806106269039, -0.1374168856037867)),
        (-0.77568377, 0.13646737),
        (-0.170337, -1.06506),
        (0.42884, -0.231345),
        (-1.62917, -0.0203968),
        (-0.761574, -0.0847596),
    ],
    "julia": [
        complex(0.001643721971153, -0.822467633298876),
        complex(-0.7756837699949401, -0.13646736999704),
        complex(
            -0.9223327810370947027656057193752719757635,
            0.3102598350874576432708737495917724836010,
        ),
        complex(-0.79, 0.15),
        complex(-0.162, 1.04),
        complex(0.3, 0.1),
        complex(-1.476, 0),
        complex(0.28, 0.008),
    ],
}


if __name__ == "__main__":
    start = time.perf_counter()

    x1 = point_collection["mandelbrot"][0][0]
    y1 = point_collection["mandelbrot"][0][1]
    # point_test(mode="m", x=x1, y=y1, zoom=10000, test_num=1, c=None, iterations=1000)

    c1 = point_collection["julia"][1]
    # point_test(mode="j", x=0, y=0, zoom=1, test_num=1, c=c1)

    # pallete_test(mode="m")
    # pallete_test(mode="j")

    x2 = point_collection["mandelbrot"][3][0]
    y2 = point_collection["mandelbrot"][3][1]
    # anim_image(
    #     mode="m",
    #     zoom_rate=8,
    #     zoom_range=101,
    #     iteration=500,
    #     x=x2,
    #     y=y2,
    #     c=None,
    #     zoom_scale=True
    # )

    c2 = point_collection["julia"][2]
    # anim_image(
    #     mode="j",
    #     zoom_rate=4,
    #     zoom_range=50,
    #     iteration=1000,
    #     x=0,
    #     y=0,
    #     c=c2,
    #     zoom_scale=False,
    # )

    x3 = point_collection["mandelbrot"][1][0]
    y3 = point_collection["mandelbrot"][1][1]
    # param_tester(mode="m", x=x3, y=y3, c=None)
    
    c3 = point_collection["julia"][0]
    # param_tester(mode="j", x=0, y=0, c=c3)

    print(f"Finished in {time.perf_counter() - start}s")
