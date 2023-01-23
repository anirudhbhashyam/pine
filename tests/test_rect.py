import os 
import sys

import functools

from typing import Callable
from typing import ParamSpec
from typing import TypeVar

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

from config_tests import *

@test_wrapper
def test_rectangle(x: int, y: int, width: int, height: int) -> int:
    # Color format: RGBA.
    im = pine.Image((SCREEN_WIDTH, SCREEN_HEIGHT))
    rect_1 = pine.Rectangle(x, y, width, height, 0xFF0000)
    rect_1.draw(im)
    im.render(
        os.path.join(
            TEST_RESULTS_DIR,
            f"rect.ppm"
        )
    )


def main() -> int:
    test_rectangle(0, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


