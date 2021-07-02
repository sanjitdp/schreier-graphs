from PIL import Image, ImageDraw
from sympy import *
from cmath import sqrt

# image dimension constants
WIDTH = 1000
HEIGHT = 1000

# complex number bound constants
RE_START = -2
RE_END = 2
IM_START = -2
IM_END = 2

# precision constants
MAX_ITERATIONS = 80
MAX_MAGNITUDE = 2

# fixed point color constants
FP_COLORS = [(200, 0, 255),  # purple
             (255, 0, 0),  # red
             (0, 255, 0),  # green
             (255, 166, 0),  # orange
             (128, 128, 128)]  # grey


# returns a tuple (n, max_distance_index) such that f^n(value) < MAX_MAGNITUDE
# and min_distance_index is the closest fixed point after MAX_ITERATIONS iterations
def julia_set(value, function, fixed_points):
    n = 0

    while n < MAX_ITERATIONS and abs(value) < MAX_MAGNITUDE:
        for i in fixed_points:
            if value == i:
                return MAX_ITERATIONS, fixed_points.index(i)
        value = function(value)
        n += 1

    distances = [abs(value - i) for i in fixed_points]
    min_distance_index = distances.index(min(distances))

    return n, min_distance_index


# create new PIL image
img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(img)


def main():
    # sympy z symbol
    z = Symbol('z')

    # For complex inputs, use i
    sym_equation = input("Equation: ").replace("i", "I")

    # Get complex roots for fixed points of equation
    fixed_point_roots = solve(eval(sym_equation + "-z"), z)

    # String Surgery to convert complex sympy roots into complex python roots
    fixed_points = []
    for fixed_point in fixed_point_roots:
        fixed_points.append(eval(str(fixed_point).replace("I", "1j")))

    # Fix input to evaluate nicely
    equation = sym_equation.replace("I", "1j")

    function = eval("(lambda z:" + equation + ')')

    print("Fixed points: ", fixed_points)
    derivative_sym_equation = diff(sym_equation)
    print("Derivative magnitudes: ",
          [abs(complex(N(derivative_sym_equation.subs(z, pt)))) for pt in fixed_points])

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            # normalize and convert (x, y) value into complex number
            c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                        IM_START + (y / HEIGHT) * (IM_END - IM_START))

            # compute n such that f^n(c) > MAX_MAGNITUDE
            # use user input function and computed fixed points
            m = julia_set(c, function, fixed_points)

            # normalizes the color into an RGB 255-scale
            colors = [255 - int(m[0] * (255 - value) / MAX_ITERATIONS)
                      for value in FP_COLORS[m[1]]]

            # draws a pixel of color associated to a fixed point with darkness associated to
            # "being in the Julia set"
            draw.point([x, HEIGHT - y], tuple(colors))

    # saves image into julia_set_output.png
    img.save("julia-set-output.png", "PNG")


if __name__ == "__main__":
    while True:
        main()
