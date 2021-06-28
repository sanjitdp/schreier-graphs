import matplotlib.pyplot as plt


def in_julia_set(f, value, maximum, n):
    for i in range(1, n):
        value = f(value)
        if abs(value) > maximum:
            return False
    return True


def polynomial(x):
    return x ** 2 - 1


if __name__ == "__main__":
    re_values = []
    im_values = []

    for re_tick in range(-2000, 2000):
        for im_tick in range(-2000, 2000):
            z = complex(re_tick / 200, im_tick / 200)
            if in_julia_set(polynomial, z, 2, 25):
                re_values.append(z.real)
                im_values.append(z.imag)
                print(z)

    plt.plot(re_values, im_values, marker=".", markersize=1)
    plt.show()
