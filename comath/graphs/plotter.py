from collections.abc import Callable
from enum import Enum

from matplotlib.pyplot import figure, show, Figure, Axes

from base import Row, NUMBER


class Colour(Enum):
    RED = "r"
    BLUE = "b"
    GREEN = "g"
    CYAN = "c"
    MAGENTA = "m"
    YELLOW = "y"
    BLACK = "k"
    WHITE = "w"


class Marker(Enum):
    NONE = ""
    POINT_MARKER = "."
    PIXEL_MARKER = ","
    CIRCLE_MARKER = "o"
    TRIANGLE_DOWN_MARKER = "v"
    TRIANGLE_UP_MARKER = "^"
    TRIANGLE_LEFT_MARKER = "<"
    TRIANGLE_RIGHT_MARKER = ">"
    TRI_DOWN_MARKER = "1"
    TRI_UP_MARKER = "2"
    TRI_LEFT_MARKER = "3"
    TRI_RIGHT_MARKER = "4"
    SQUARE_MARKER = "s"
    PENTAGON_MARKER = "p"
    STAR_MARKER = "*"
    HEXAGON1_MARKER = "h"
    HEXAGON2_MARKER = "H"
    PLUS_MARKER = "+"
    X_MARKER = "x"
    DIAMOND_MARKER = "D"
    THIN_DIAMOND_MARKER = "d"
    VERTICAL_LINE_MARKER = "|"
    HORIZONTAL_LINE_MARKER = "_"


class LineStyle(Enum):
    NONE = ""
    SOLID = "-"
    DASHED = "--"
    DASH_DOT = "-."
    DOTTED = ":"


class Plot:
    def __init__(self, start: NUMBER, finish: NUMBER):
        self.start: NUMBER = start
        self.finish: NUMBER = finish

        self.figure: Figure = figure()
        self.axes: Axes = self.figure.add_subplot(1, 1, 1)
        self.axes.spines["left"].set_position("center")
        self.axes.spines["bottom"].set_position("zero")
        self.axes.spines["right"].set_color("none")
        self.axes.spines["top"].set_color("none")
        self.axes.xaxis.set_ticks_position("bottom")
        self.axes.yaxis.set_ticks_position("left")

    def add_equation(self, equation: Callable[[Row], Row], colour: Colour, label: str = None,
                     line_style: LineStyle = LineStyle.NONE, marker: Marker = Marker.NONE):
        x = Row.linearly_spaced(self.start, self.finish, 100)
        self.axes.plot(x, equation(x), colour.value + marker.value + line_style.value, label=label)

    def add_points(self, xs: Row | NUMBER, ys: Row | NUMBER, colour: Colour, marker: Marker, label: str = None):
        self.axes.plot(xs, ys, colour.value + marker.value, label=label)

    def show(self):
        self.axes.legend()
        show()
