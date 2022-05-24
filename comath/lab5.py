from enum import Enum
from decimal import Decimal
from math import sin

from base import NUMBER, input_menu, input_decimal
from equations import functions
from graphs import ODESolver, EulerODES, EulerPlusODES, RungeKuttaODES, MilneODES, AdamsODES
from graphs import Plot, Colour, Marker  # , NewtonInterpolator


class ODESolverMenu(Enum):
    EULER = "Euler's method"
    EULER_PLUS = "Advanced Euler's method"
    RUNGE_KUTTA = "Runge Kutta's method (fourth order)"
    MILNE = "Milne's multistep method"
    ADAMS = "Adams' multistep method"
    ALL = "Show all at once"

    def solver(self, step_size: NUMBER, point_count: int):
        match self:
            case ODESolverMenu.EULER:
                return EulerODES(step_size, point_count)
            case ODESolverMenu.EULER_PLUS:
                return EulerPlusODES(step_size, point_count)
            case ODESolverMenu.RUNGE_KUTTA:
                return RungeKuttaODES(step_size, point_count)
            case ODESolverMenu.MILNE:
                return MilneODES(RungeKuttaODES, step_size, point_count)
            case ODESolverMenu.ADAMS:
                return AdamsODES(RungeKuttaODES, step_size, point_count)


class ODEExample(Enum):
    Y_ONLY = "Equation 1: y' = y"
    X_ONLY = "Equation 2: y' = x"
    SIN_X = "Equation 3: y' = sin(x)"
    BOTH = "Equation 4: y' = 0.5xy"

    def equation(self, x: Decimal, y: Decimal) -> Decimal:
        match self:
            case ODEExample.Y_ONLY:
                return y
            case ODEExample.X_ONLY:
                return x
            case ODEExample.SIN_X:
                return Decimal.from_float(sin(x))
            case ODEExample.BOTH:
                return x * y / Decimal(2)

    def _solution(self):
        match self:
            case ODEExample.Y_ONLY:
                return functions.ExponentEquation()
            case ODEExample.X_ONLY:
                return (functions.SquareEquation() + Decimal(2)) / Decimal(2)
            case ODEExample.SIN_X:
                return -functions.TrigonometricEquation(functions.TrigonometricEquationType.COS)
            case ODEExample.BOTH:
                return functions.ExponentEquation()(functions.SquareEquation() / Decimal(4))

    def solution(self, x_0: Decimal, y_0: Decimal):
        result = self._solution()
        return result - (result.function(x_0) - y_0)


def solve_one(plot: Plot, solver: ODESolver, x: Decimal, y: Decimal, equation: ODEExample, colour: Colour):
    xs, ys = solver.solve_as_rows(equation.equation, x, y)
    # ni = NewtonInterpolator(xs, ys)
    # plot.add_equation(ni.interpolate_row, colour, solver.__class__.__name__[:-4])
    plot.add_points(xs, ys, colour, Marker.NONE, label=solver.__class__.__name__[:-4])


if __name__ == "__main__":
    solver: ODESolverMenu = input_menu(ODESolverMenu, "Enter the preferred solver: ")
    ode: ODEExample = input_menu(ODEExample, "Enter the equation to solve: ")
    x, y = input_decimal("Enter the condition's x: "), input_decimal("Enter the condition's y: ")
    a, b = input_decimal("Enter the starting x: "), input_decimal("Enter the finishing x: ")
    step_size = input_decimal("Enter the step size: ")
    point_count = int((b - a) // step_size)

    plot = Plot(a, b)
    if solver == ODESolverMenu.ALL:
        solvers = [
            (ODESolverMenu.EULER, Colour.RED),
            (ODESolverMenu.EULER_PLUS, Colour.GREEN),
            (ODESolverMenu.RUNGE_KUTTA, Colour.BLUE),
            (ODESolverMenu.MILNE, Colour.YELLOW),
            (ODESolverMenu.ADAMS, Colour.CYAN),
        ]
        for one_solver, colour in solvers:
            solve_one(plot, one_solver.solver(step_size, point_count), x, y, ode, colour)
    else:
        solve_one(plot, solver.solver(step_size, point_count), x, y, ode, Colour.GREEN)
    plot.add_equation(ode.solution(x, y).function_row, Colour.BLACK, label="Solution")
    plot.add_points(x, y, Colour.MAGENTA, Marker.X_MARKER)
    plot.show()
