from tifffile import imread, imsave
from subprocess import call

import numpy as np
import sys


def main():
    image = imread(sys.argv[1])
    s = "model2point {} tmp.point >/dev/null".format(sys.argv[2])
    call(s, shell=True)
    points = np.loadtxt('tmp.point', dtype=int)
    points[:, 1] = image.shape[-1] - points[:, 1]
    m0 = np.median(image[0])
    m1 = np.median(image[1])
    for i, item in enumerate(points):
        v1 = value_area(image[0] / m0, item, 2)
        v2 = value_area(image[1] / m1, item, 2)
        print("{} v1 v2 v1/v2 {} {} {}".format(i, v1, v2, v1 / v2))


def value_area(image, center, radius):
    d = image[center[1] - 10:center[1] + 10, center[0] - 10:center[0] + 10]
    d = d.astype(np.uint16)
    imsave('test.tif', d)
    value = 0.0
    count = 0
    for i in range(-1 * radius, 1 * radius):
        for j in range(-1 * radius, 1 * radius):
            if i ** 2 + j ** 2 < radius ** 2:
                value += image[center[0] + i][center[1] + j]
                count += 1
    return value / count


if __name__ == '__main__':
    main()
