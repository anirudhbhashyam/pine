import os
import sys

import itertools

from typing import Generator

CPD = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        *(2 * [os.pardir])
    )
)

sys.path.append(
    os.path.join(CPD, "src")
)

import pine

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256


def diagonal_rects() -> Generator[pine.Rectangle, None, None]:
    x, y = 0, 0
    w, h = 5, 5
    c = 0x7BEFE6
    while True:
        yield pine.Rectangle(x, y, w, h, c)
        x += w
        y += h
        w += 2
        h += 2
        c += 0x0A0A05


def main() -> int:
    im = pine.Image((256, 256))
    for rect in itertools.islice(diagonal_rects(), 20):
        rect.draw(im)

    im.render("rects.ppm")

    return 0


if __name__ == "__main__":
    sys.exit(main())