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

SCREEN_WIDTH = 4
SCREEN_HEIGHT = 4


def create_artificial_image(w: int, h: int) -> list[int]:
    return [0 for _ in range(w * h)]

@pytest.mark.parametrize(
    ("x", "y", "width", "height"),
    [
        (0, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        (2, 4, 3, 4)
    ] 
)
def test_rectangle(x: int, y: int, width: int, height: int) -> int:
    # Color format: RGBA.
    im = pine.Image((SCREEN_WIDTH, SCREEN_HEIGHT))
    rect_1 = pine.Rectangle(x, y, width, height, 0xFF0000)
    rect_1.draw(im)

    a_im = create_artificial_image(SCREEN_WIDTH, SCREEN_HEIGHT)

    for j in range(y, min(y + height, SCREEN_HEIGHT)):
        for i in range(x, min(x + width, SCREEN_WIDTH)):
            a_im[j * SCREEN_WIDTH + i] = 0xFF0000

    assert a_im == im.get_pixel_data()


