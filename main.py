import os 
import sys

CPD = os.path.abspath(
    os.path.join(
        __file__,
        *([os.pardir] * 1)
    )
)

sys.path.append(
    os.path.join(CPD, "src")
)

import pine


def main() -> int:
    # Color format: RGBA.
    im = pine.Image((1920, 1080))
    rect_1 = pine.Rectangle(100, 100, 100, 100, 0xFF0000)
    rect_2 = pine.Rectangle(100, 500, 300, 200, 0xAA00AA)
    circle_1 = pine.Circle(300, 600, 10, 0xFF0000)
    circle_2 = pine.Circle(400, 600, 10, 0xFF0000)
    line_1 = pine.Line(300, 600, 500, 800, 0xFFAAAA)
    triangle_1 = pine.Triangle(300, 600, 500, 800, 500, 400, 0xAAEEAA)
    im.fill(0x000000)
    rect_1.draw(im)
    rect_2.draw(im)
    circle_1.draw(im)
    circle_2.draw(im)
    line_1.draw(im)
    triangle_1.draw(im)
    print(triangle_1._is_point_inside(400, 600))
    im.render("test.ppm")
    return 0


if __name__ == "__main__":
    raise sys.exit(main())