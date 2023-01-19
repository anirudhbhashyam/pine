from typing import Generator 

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


class Rectangle:
    def __init__(self, x: int, y: int, width: int, height: int, color: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, im: Image) -> None:
        for y in range(self.y, min(self.y + self.height, im.height)):
            for x in range(self.x, min(self.x + self.width, im.width)):
                im.set_color(x, y, self.color)

class Circle:
    def __init__(self, x: int, y: int, r: int, color: int) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def draw(self, im: Image) -> None:
        x_min, x_max = self.x - self.r, self.x + self.r
        y_min, y_max = self.y - self.r, self.y + self.r

        for py in range(y_min, y_max):
            for px in range(x_min, x_max):
                if (px - self.x) ** 2 + (py - self.y) ** 2 <= self.r ** 2:
                    im.set_color(py, px, self.color)

class Line:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.color = color

    def draw(self, im: Image) -> None:
        dx = self.x2 - self.x1
        dy = abs(self.y2 - self.y1)
        yi = -1 if dy < 0 else 1
        D = (2 * dy) - dx
        y = self.y1

        for x in range(self.x1, self.x2):
            im.set_color(x, y, self.color)
            if D > 0:
                y = y + yi
                D += (2 * (dy - dx))
            else:
                D += 2 * dy




