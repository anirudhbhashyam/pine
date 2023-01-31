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

import pine

TEST_FIGS_DIR = "./test_figs"


def test_lines() -> NoReturn:
    lines_im = pine.Image.from_file(os.path.join(TEST_FIGS_DIR, "lines.ppm"))
    image_width, image_height = lines_im.width, lines_im.height
    im = pine.Image((image_width, image_height))
    l1 = pine.Line(0, 0, image_width, image_height, 0xFF0000)
    l2 = pine.Line(image_width, 0, 0, image_height, 0x00FF00)
    l3 = pine.Line(image_width // 2, 0, image_width // 2, image_height, 0x0000FF)
    l4 = pine.Line(0, image_height // 2, image_width, image_height // 2, 0x00AAFF)
    l1.draw(im)
    l2.draw(im)
    l3.draw(im)
    l4.draw(im)

    assert im == lines_im