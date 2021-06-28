from PIL import Image, ImageDraw

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

# fixed points
FIXED_POINTS = [1j, -1j, 1, -1]

# fixed point color constants
FP_COLORS = [(200, 0, 255),  # purple, i
             (255, 0, 0),  # red, -i
             (0, 255, 0),  # green, 1
             (255, 166, 0)]  # orange, -1

# function whose Julia set to compute
FUNCTION = (lambda z: (5 * z - z ** 5) / 4)


# returns a tuple (n, max_distance_index) such that f^n(value) < MAX_MAGNITUDE
# and min_distance_index is the closest fixed point after MAX_ITERATIONS iterations
def julia_set(value):
    n = 0
    while n < MAX_ITERATIONS and abs(value) < MAX_MAGNITUDE:
        value = FUNCTION(value)
        n += 1

    distances = [abs(value - i) for i in FIXED_POINTS]
    min_distance_index = distances.index(min(distances))

    return n, min_distance_index


# create new PIL image
img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(img)

for x in range(0, WIDTH):
    for y in range(0, HEIGHT):
        # normalize and convert (x, y) value into complex number
        c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                    IM_START + (y / HEIGHT) * (IM_END - IM_START))

        # compute n such that f^n(c) > MAX_MAGNITUDE
        m = julia_set(c)

        # normalizes the color into an RGB 255-scale
        colors = [255 - int(m[0] * (255 - value) / MAX_ITERATIONS)
                  for value in FP_COLORS[m[1]]]

        # draws a pixel of color associated to a fixed point with darkness associated to
        # "being in the Julia set"
        draw.point([x, y], tuple(colors))

# saves image into julia_set_output.png
img.save("julia_set_output.png", "PNG")
