import sys

import copy 

from typing import Generator 
from typing import Iterable

try:
    from typing import Self
except ImportError:
    from typing import TypeVar
    Self = TypeVar("Self")
    

from dataclasses import dataclass


class Image:
    def __init__(self, size: tuple[int, int]) -> None:
        self.width, self.height = size
        self.image = [0 for _ in range(self.width * self.height)]

    @classmethod
    def from_file(cls, file: str) -> Self:
        file_gen = cls._read_ppm_file(file)
        width, height = next(file_gen)
        im = cls((width, height))
        im.image = [cls.pack_rgb(s) for s in file_gen]
        return im
    
    @classmethod
    def from_data(cls, width: int, height: int, data: list[int]) -> Self:
        im = cls((width, height))
        im.image = data
        return im

    @staticmethod
    def pack_rgb(color: Iterable[int]) -> int:
        r, g, b, *_ = color
        return ((r & 0xFF) << 8 * 2) + ((g & 0xFF) << 8 * 1) + ((b & 0xFF) << 8 * 0)

    def get_pixel_data(self) -> list[int]:
        return self.image

    def set_color(self, row: int, col: int, color: int) -> None:
        if (row < 0 or row >= self.width or col < 0 or col >= self.height):
            return
        self.image[col * self.width + row] = color

    def image_view(self) -> Generator[int, None, None]:
        for j in range(self.height):
            for i in range(self.width):
                yield self.image[j * self.width + i]

    def fill(self, color: int) -> None:
        for j in range(self.height):
            for i in range(self.width):
                self.set_color(i, j, color)

    def render(self, path: str) -> None:
        with open(path, "w") as f:
            f.write("P3\n")
            f.write(f"{self.width} {self.height}\n")
            f.write(f"255\n")

            for pixel in self.image_view():
                r, g, b = (pixel >> 8 * 2) & 0xFF, (pixel >> 8 * 1) & 0xFF, (pixel >> 8 * 0) & 0xFF
                f.write(f"{r} {g} {b}\n")

    def __len__(self) -> int:
        return len(self.image)

    def __eq__(self, other: "Self") -> bool:
        # Check for image length (all pixels.)
        if len(self) != len(other):
            return False

        # Check if pixel values are the same.
        for pixel_1, pixel_2 in zip(self.image_view(), other.image_view(), strict = True):
            if pixel_1 != pixel_2:
                return False
        return True
    
    @staticmethod
    def _read_ppm_file(file: str) -> Generator[int, None, None]:
         with open(file, "r") as f:
            # Skip the P3 header.
            next(f)
            width, height = map(int, next(f).split(" "))
            yield width, height
            # Skip the bit depth.
            next(f)
            for pixel in f:
                yield [int(x) for x in pixel.split(" ")]


@dataclass
class Rectangle:
    x: int
    y: int
    width: int
    height: int
    color: int

    def draw(self, im: Image) -> None:
        for y in range(self.y, min(self.y + self.height, im.height)):
            for x in range(self.x, min(self.x + self.width, im.width)):
                im.set_color(x, y, self.color)


@dataclass
class Circle:
    x: int
    y: int
    r: int
    color: int

    def draw(self, im: Image) -> None:
        x_min, x_max = self.x - self.r, self.x + self.r
        y_min, y_max = self.y - self.r, self.y + self.r

        for py in range(y_min, y_max):
            for px in range(x_min, x_max):
                if (px - self.x) ** 2 + (py - self.y) ** 2 <= self.r ** 2:
                    im.set_color(px, py, self.color)


@dataclass
class Line:
    x1: int
    y1: int
    x2: int
    y2: int
    color: int

    def draw(self, im: Image) -> None:
        x = copy.deepcopy(self.x1)
        y = copy.deepcopy(self.y1)
        dx = abs(self.x2 - self.x1)
        sx = 1 if (self.x1 < self.x2) else -1
        dy = -abs(self.y2 - self.y1)
        sy = 1 if (self.y1 < self.y2) else -1
        error = dx + dy
        
        while True:
            im.set_color(x, y, self.color)
            if (x == self.x2) and (y == self.y2): 
                break
            e2 = error << 1
            if e2 >= dy:
                if (x == self.x2): 
                    break
                error += dy
                x += sx
            if e2 <= dx:
                if (y == self.y2): 
                    break
                error += dx
                y += sy

    def _slope(self) -> int | None:
        try:
            return (self.y2 - self.y1) / (self.x2 - self.x1)
        except ZeroDivisionError as e:
            print("WARNING: Attempted to calculate the slope of a vertical line.", file = sys.stderr)
            return None

    def _intercept(self) -> int | None:
        if self._slope() is None:
            return None
        return self.y1 - self._slope() * self.x1

    def __call__(self, x: int) -> int:
        return self._slope() * x + self._intercept()


@dataclass
class Triangle:
    x1: int
    y1: int
    x2: int
    y2: int
    x3: int
    y3: int
    color: int = 0xAAFFAA
    _lines: list[Line] = None

    def __post_init__(self) -> None:
        self._lines = [
            Line(self.x1, self.y1, self.x2, self.y2, self.color),
            Line(self.x2, self.y2, self.x3, self.y3, self.color),
            Line(self.x3, self.y3, self.x1, self.y1, self.color),
        ]

    def draw(self, im: Image) -> None:
        for line in self._lines: 
            line.draw(im)
        
        # Render the inside.
        x_min, *_, x_max = sorted((self.x1, self.x2, self.x3))
        y_min, *_, y_max = sorted((self.y1, self.y2, self.y3))

        for py in range(y_min, y_max):
            for px in range(x_min, x_max):
                if self._is_point_inside(px, py):
                    im.set_color(px, py, self.color)

    # def _area(self) -> None:
    #     # Area is actually half this. Only used for queries.
    #     return abs(
    #           self.x1 * (self.y2 - self.y3)
    #         + self.x2 * (self.y3 - self.y1)
    #         + self.x3 * (self.y1 - self.y3)
    #     )
    
    def _is_point_inside(self, x: int, y: int) -> bool:
        a_num = (self.y3 - self.y1) * (x - self.x1) + (self.y1 - y) * (self.x3 - self.x1)
        b_num = (self.y2 - self.y1) * (x - self.x1) + (self.y1 - y) * (self.x2 - self.x1)
        dem = (self.x2 - self.x1) * (self.y3 - self.y1) - (self.y2 - self.y1) * (self.x3 - self.x1)

        a = a_num / dem
        b = -b_num / dem

        return ( a > 0 and b > 0 and a + b < 1 )

