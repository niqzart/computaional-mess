from decimal import Decimal

from equations import ExponentEquation, SquareEquation
from graphs import EulerODES, EulerPlusODES, RungeKuttaODES, MilneODES, AdamsODES
from graphs import Plot, Colour, Marker  # , NewtonInterpolator

if __name__ == "__main__":
    step_size, point_count = Decimal("0.1"), 50

    odes = [
        (EulerODES(step_size, point_count), Colour.RED),
        (EulerPlusODES(step_size, point_count), Colour.GREEN),
        (RungeKuttaODES(step_size, point_count), Colour.BLUE),
        (MilneODES(RungeKuttaODES, step_size, point_count), Colour.YELLOW),
        (AdamsODES(RungeKuttaODES, step_size, point_count), Colour.CYAN),
    ]
    equations = [
        (lambda x, y: y, 0, 1, ExponentEquation()),
        (lambda x, y: y * x / Decimal(2), 0, 1, ExponentEquation()(SquareEquation() / Decimal(4))),
        (lambda x, y: x, 0, 1, (SquareEquation() + Decimal(2)) / Decimal(2)),
    ]

    for e, x, y, f in equations:
        plot = Plot(0, 5)
        for i, (solver, colour) in enumerate(odes):
            xs, ys = solver.solve_as_rows(e, x, y)
            # ni = NewtonInterpolator(xs, ys)
            # print(xs, ys, f.function_row(xs), sep="\n")
            plot.add_points(xs, ys, colour, Marker.NONE, label=solver.__class__.__name__[:-4])
            # plot.add_equation(ni.interpolate_row, colour, solver.__class__.__name__[:-4])
        plot.add_equation(f.function_row, Colour.BLACK, label="original")
        plot.add_points(x, y, Colour.MAGENTA, Marker.X_MARKER)
        plot.show()
