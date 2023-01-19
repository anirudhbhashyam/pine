import os 
import sys

CPD = os.path.join(
    os.path.abspath(__file__),
    *([os.pardir] * 1)
)

sys.path.append(
    os.path.join(CPD, "src")
)

from src import pine


def main() -> int:
    # Color format: RGBA.
    im = pine.Image((800, 600))
    rect_1 = pine.Rectangle(100, 100, 100, 100, 0xFF0000)
    rect_2 = pine.Rectangle(100, 500, 300, 200, 0xAA00AA)
    circle_1 = pine.Circle(400, 300, 100, 0xFFFF00)
    im.fill(0x000000)
    rect_1.draw(im)
    rect_2.draw(im)
    circle_1.draw(im)
    im.render("test.ppm")
    return 0


if __name__ == "__main__":
    raise sys.exit(main())