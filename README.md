# Fractal Geometry Creator

## Mandelbrot and Julia sets created and visualized in Python

A set of scripts to create and visualize Mandelbrot and Julia sets. The `fractal_maker.py` script will create an image or images based on the selected function. 

Options include:
- `point_test`
- `pallete_test`
- `anim_image`
- `param_tester`

The options are selected by un-commenting the respective line from the entry point function at the bottom of the `fractal_maker` script.

## Example:
Test the point -0.7756837699949401 -0.13646736999704i at a zoom level of 10,000x with a cutoff iteration value of 1,000:
```py
# fractal_maker.py
if __name__ == "__main__":
    start = time.perf_counter()

    x1 = point_collection["mandelbrot"][0][0]
    y1 = point_collection["mandelbrot"][0][1]

    point_test(mode="m", x=x1, y=y1, zoom=10000, test_num=1, iterations=1000)

    print(f"Finished in {time.perf_counter() - start}s")
```
Result:

![Example 1](https://github.com/brad90four/mandelbrot/blob/main/m_example_1.png)

## Animation Example:
Create a series of images at higher zoom levels, and run the `animator` script to create an animation. 
```py
# fractal_maker.py
if __name__ == "__main__":
    start = time.perf_counter()

    x2 = point_collection["mandelbrot"][3][0]
    y2 = point_collection["mandelbrot"][3][1]
    anim_image(
        mode="m",
        zoom_rate=2,
        zoom_range=10,
        iteration=100,
        x=x2,
        y=y2,
        zoom_scale=True
    )

    print(f"Finished in {time.perf_counter() - start}s")
```

And once the images are created:
```py
# animator.py

if __name__ == "__main__":
    mp4("test1", 10)
```

Result:

![Example 2](https://github.com/brad90four/mandelbrot/blob/main/test1.mp4)