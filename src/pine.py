import copy 

from typing import Generator 

from dataclasses import dataclass


class Image:
    def __init__(self, size: tuple[int, int]) -> None:
        self.width, self.height = size
        self.image = [0 for _ in range(self.width * self.height)]

    def set_color(self, row: int, col: int, color: int) -> None:
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
                    im.set_color(py, px, self.color)

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


@dataclass
class Triangle:
    x1: int
    y1: int
    x2: int
    y2: int
    x3: int
    y3: int
    color: int
    _lines: list[Line] = None

    def __post_init__(self) -> None:
        self._lines = [
            Line(self.x1, self.y1, self.x2, self.y2, self.color),
            Line(self.x2, self.y2, self.x3, self.y3, self.color),
            # Line(self.x3, self.y3, self.x1, self.y1, self.color),
        ]

    def draw(self, im: Image) -> None:
        for line in self._lines: 
            line.draw(im)

