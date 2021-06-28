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

# function whose Julia set to compute
FUNCTION = (lambda z: (5 * z - z ** 5) / 4)


# returns n such that f^n(value) <
def julia_set(value):
    n = 0
    while n < MAX_ITERATIONS and abs(value) < MAX_MAGNITUDE:
        value = FUNCTION(value)
        n += 1
    return n


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
        color = 255 - int(m * 255 / MAX_ITERATIONS)

        # draws a grayscale pixel with n such that f^n(c) > MAX_MAGNITUDE
        draw.point([x, y], (color, color, color))

# saves image into julia_set_output.png
img.save("julia_set_output.png", "PNG")
