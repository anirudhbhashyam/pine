import os
import sys

import pytest

CPD = os.path.abspath(
    os.path.join(
        __file__,
        *([os.pardir] * 2)
    )
)

sys.path.append(
    os.path.join(CPD, "src")
)

import pine

TEST_FIGS_DIR = "test_figs"

if not os.path.exists(TEST_FIGS_DIR):
    os.makedirs(TEST_FIGS_DIR)

IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256


def generate_line_cases() -> None:
    im = pine.Image((IMAGE_WIDTH, IMAGE_HEIGHT))
    l1 = pine.Line(0, 0, IMAGE_WIDTH, IMAGE_HEIGHT, 0xFF0000)
    l2 = pine.Line(IMAGE_WIDTH, 0, 0, IMAGE_HEIGHT, 0x00FF00)
    l3 = pine.Line(IMAGE_WIDTH // 2, 0, IMAGE_WIDTH // 2, IMAGE_HEIGHT, 0x0000FF)
    l4 = pine.Line(0, IMAGE_HEIGHT // 2, IMAGE_WIDTH, IMAGE_HEIGHT // 2, 0x00AAFF)
    l1.draw(im)
    l2.draw(im)
    l3.draw(im)
    l4.draw(im)
    im.render(os.path.join(TEST_FIGS_DIR, "lines.ppm"))


def main() -> int:
    generate_line_cases()
    return 0


if __name__ == "__main__":
    sys.exit(main())