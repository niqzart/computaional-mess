from base import Row
from equations import PolynomialEquation
from graphs import Approximator, ApproximationFunction, Plot, Colour, Marker, Interpolator, NewtonInterpolator

if __name__ == "__main__":
    eq = PolynomialEquation(1, -5, 6, 3, -2)
    xs = Row([i for i in range(-5, 6)])
    ys = eq.function_row(xs)

    t: Approximator = ApproximationFunction.FULL_SQUARE.approximator()
    i, r = t.fit_and_exclude(xs, ys)
    ni: Interpolator = NewtonInterpolator(xs, ys)

    print(i, r)
    print(t.coefficients)
    print(ys)
    print(t.predict_row(xs))

    plot = Plot(xs[0] - 1, xs[-1] + 1)
    plot.add_equation(ni.interpolate_row, Colour.GREEN, "interpolation")
    plot.add_equation(t.predict_row, Colour.RED, "approximation")
    plot.add_equation(eq.function_row, Colour.BLUE, "original")
    plot.add_points(xs, ys, Colour.YELLOW, Marker.CIRCLE_MARKER)
    plot.add_points(xs[i], ys[i], Colour.BLACK, Marker.CIRCLE_MARKER)
    plot.show()
