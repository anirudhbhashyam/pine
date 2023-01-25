import os 
import sys

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

SCREEN_WIDTH = 16
SCREEN_HEIGHT = 16


def test_eq_im() -> int:
    # Color format: RGBA.
    im_1 = pine.Image((SCREEN_WIDTH, SCREEN_HEIGHT))
    im_2 = pine.Image((SCREEN_WIDTH, SCREEN_HEIGHT))

    assert im_1 == im_2

    rect_1 = pine.Rectangle(0, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0xFF0000)
    rect_2 = pine.Rectangle(0, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0xFF0000)
    rect_1.draw(im_1)
    rect_2.draw(im_2)

    assert im_1 == im_2
