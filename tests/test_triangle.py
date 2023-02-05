import os 
import sys

from typing import NoReturn

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

TEST_FIGS_DIR = "test_figs"

import pine


def test_triangle() -> NoReturn:
    triangles_im = pine.Image.from_file(os.path.join(TEST_FIGS_DIR, "triangles.ppm"))
    image_width, image_height = triangles_im.width, triangles_im.height
    im = pine.Image((image_width, image_height))
    t1 = pine.Triangle(0, 0, 0, image_width, image_width // 2, image_height, 0xAAFFEE)
    t2 = pine.Triangle(image_width, 0, image_width, image_height, image_width // 2, image_height, 0xBBFFBB)
    t3 = pine.Triangle(image_width // 2, 0, image_width // 2 - 100, 0, image_width // 2 - 50, 100, 0xFFBBBB)
    t4 = pine.Triangle(image_width // 2, 0, image_width // 2 + 100, 0, image_width // 2 + 50, 100, 0xFFBBFF)
    t1.draw(im)
    t2.draw(im)
    t3.draw(im)
    t4.draw(im)
    
    assert im == triangles_im