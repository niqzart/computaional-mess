from decimal import Decimal
from enum import Enum
from math import sin

from base import NUMBER, input_menu, input_decimal
from equations import functions, AnyEquation
from graphs import ODESolver, EulerODES, EulerPlusODES, RungeKuttaODES, MilneODES, AdamsODES, NewtonInterpolator
from graphs import Plot, Colour, Marker


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
    Y_ONLY = "y' = y"
    X_ONLY = "y' = x"
    SIN_X = "y' = sin(x)"
    BOTH = "y' = 0.5xy"

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

    def solution(self, x_0: Decimal, y_0: Decimal) -> AnyEquation:
        match self:
            case ODEExample.Y_ONLY:
                result = functions.ExponentEquation()
                c: Decimal = y_0 / result.function(x_0)
                return result * c
            case ODEExample.X_ONLY:
                result = (functions.SquareEquation() + Decimal(2)) / Decimal(2)
                c: Decimal = y_0 - result.function(x_0)
                return result + c
            case ODEExample.SIN_X:
                result = -functions.TrigonometricEquation(functions.TrigonometricEquationType.COS)
                c: Decimal = y_0 - result.function(x_0)
                return c + result
            case ODEExample.BOTH:
                result = functions.ExponentEquation()(functions.SquareEquation() / Decimal(4))
                c: Decimal = y_0 / result.function(x_0)
                return result * c


def solve_one(plot: Plot, solver: ODESolver, x: Decimal, y: Decimal, equation: ODEExample,
              colour: Colour, point_marker: Marker = Marker.CIRCLE_MARKER, point_color: Colour = Colour.RED):
    xs, ys = solver.solve_as_rows(equation.equation, x, y)
    ni = NewtonInterpolator(xs, ys)
    plot.add_equation(ni.interpolate_row, colour, "interpolated")
    if xs.size < 30 and point_marker != Marker.NONE:
        x0, y0 = xs.pop(0), ys.pop(0)
        plot.add_points(xs, ys, point_color, point_marker, label="solved")
        plot.add_points(x0, y0, Colour.MAGENTA, point_marker, label="condition")


if __name__ == "__main__":
    solver: ODESolverMenu = ODESolverMenu.RUNGE_KUTTA  # input_menu(ODESolverMenu, "Enter the preferred solver: ")
    ode: ODEExample = input_menu(ODEExample, "Enter the equation to solve: ")
    x = input_decimal("Enter the condition's x: ")
    y = input_decimal("Enter the condition's y: ")
    b = input_decimal("Enter the finishing x: ")
    step_size = input_decimal("Enter the step size: ")
    point_count = int((b - x) // step_size)

    plot = Plot(x, b)
    plot.add_equation(ode.solution(x, y).function_row, Colour.BLACK, label="solution")
    if solver == ODESolverMenu.ALL:
        solvers = [
            (ODESolverMenu.EULER, Colour.RED),
            (ODESolverMenu.EULER_PLUS, Colour.GREEN),
            (ODESolverMenu.RUNGE_KUTTA, Colour.BLUE),
            (ODESolverMenu.MILNE, Colour.YELLOW),
            (ODESolverMenu.ADAMS, Colour.CYAN),
        ]
        for one_solver, colour in solvers:
            solve_one(plot, one_solver.solver(step_size, point_count), x, y, ode, colour, Marker.NONE)
    else:
        solve_one(plot, solver.solver(step_size, point_count), x, y, ode, Colour.GREEN)
    plot.show()
