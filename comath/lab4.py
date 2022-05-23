from base import Row
from equations import PolynomialEquation
from graphs import Approximator, ApproximationFunction, Plot, Colour, Marker


if __name__ == "__main__":
    t: Approximator = ApproximationFunction.FULL_SQUARE.approximator()
    eq = PolynomialEquation(1, -5, 6)
    xs = Row([i for i in range(-5, 6)])
    ys = eq.function_row(xs)
    i, r = t.fit_and_exclude(xs, ys)
    print(i, r)
    print(t.coefficients)
    print(ys)
    print(t.predict_row(xs))

    plot = Plot()
    plot.add_equation(t.predict_row, xs[0] - 1, xs[-1] + 1, Colour.RED, "approximation")
    plot.add_equation(eq.function_row, xs[0] - 1, xs[-1] + 1, Colour.BLUE, "original")
    plot.add_points(xs, ys, Colour.YELLOW, Marker.CIRCLE_MARKER)
    plot.add_points(xs[i], ys[i], Colour.BLACK, Marker.CIRCLE_MARKER)
    plot.show()
