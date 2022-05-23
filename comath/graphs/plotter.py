from collections.abc import Callable
from enum import Enum

from matplotlib.pyplot import figure, plot, show, Figure, Axes, axis, legend

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


def setup_pyplot():
    fig: Figure = figure()
    ax: Axes = fig.add_subplot(1, 1, 1)
    ax.spines["left"].set_position("center")
    ax.spines["bottom"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")


def plot_equation(equation: Callable[[Row], Row], start: NUMBER, finish: NUMBER, colour: Colour,
                  label: str = None, line_style: LineStyle = LineStyle.NONE, marker: Marker = Marker.NONE):
    x = Row.linearly_spaced(start, finish, 100)
    plot(x, equation(x), colour.value + marker.value + line_style.value, label=label)


def plot_points(xs: Row | NUMBER, ys: Row | NUMBER, colour: Colour, marker: Marker, label: str = None):
    plot(xs, ys, colour.value + marker.value, label=label)


def show_with_legend():
    legend()
    show()
