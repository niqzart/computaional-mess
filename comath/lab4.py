from decimal import Decimal, DecimalException
from enum import Enum

from base import Row, input_bool, checked_input, input_decimal, input_menu, beautify_decimal
from equations import functions, AnyEquation
from graphs import Plot, Colour, Marker, NewtonInterpolator, distort_row


class ExampleFunction(Enum):
    SQUARE_FUNCTION = "Square function: ax² + bx + c"
    POLYNOMIAL_FUNCTION = "Polynomial function: ∑(aₖ xᵏ) for k ∈ [0, n]"
    INVERSE_FUNCTION = "Inverse function: 1 / (kx + b)"
    SIN_FUNCTION = "Sin function: sin(x)"
    LOG_FUNCTION = "Log function: ln(x)"
    EXP_FUNCTION = "Exponential: exp(x)"


def coefficients_check(line: str) -> list[Decimal] | None:
    try:
        result = [Decimal(c) for c in line.replace(",", ".").strip().split()]
        return None if result[0] == 0 else result
    except DecimalException:
        return None


SINC_FUNCTION = functions.TrigonometricEquation(functions.TrigonometricEquationType.SIN) / functions.LinearEquation()
INVERSE_FUNCTION = Decimal(1) / functions.LinearEquation()
OSCILLATING_FUNCTION = functions.TrigonometricEquation(functions.TrigonometricEquationType.SIN)(INVERSE_FUNCTION)


if __name__ == "__main__":
    function: AnyEquation

    match input_menu(ExampleFunction, "Enter the function to integrate: "):
        case ExampleFunction.SQUARE_FUNCTION:
            a = input_decimal("Enter a ≠ 0: ", lambda x: None if x == 0 else x)
            b = input_decimal("Enter b: ")
            c = input_decimal("Enter c: ")
            function = functions.SquareEquation(a, b, c)
        case ExampleFunction.POLYNOMIAL_FUNCTION:
            prompt = "Enter all coefficients (space separated, starting with the senior one): "
            coefficients = checked_input(prompt, coefficients_check)
            function = functions.PolynomialEquation(*coefficients)
        case ExampleFunction.INVERSE_FUNCTION:
            k = input_decimal("Enter k ≠ 0: ", lambda x: None if x == 0 else x)
            b = input_decimal("Enter b: ")
            function = Decimal(1) / functions.LinearEquation(k, b)
        case ExampleFunction.SIN_FUNCTION:
            function = functions.TrigonometricEquation(functions.TrigonometricEquationType.SIN)
        case ExampleFunction.LOG_FUNCTION:
            function = functions.LogarithmEquation()
        case ExampleFunction.EXP_FUNCTION:
            function = functions.ExponentEquation()

    xs = Row([i for i in range(-5, 6) if i != 0])
    ys = function.function_row(xs)
    xs = Row([xs[i] for i in range(xs.size) if ys[i] is not None])
    ys = Row([y for y in ys if y is not None])
    ys = distort_row(ys, 0)
    [print(beautify_decimal(xs[i].quantize(Decimal("0.01"))), beautify_decimal(ys[i].quantize(Decimal("0.01"))), sep=", ") for i in range(xs.size)]

    ni: NewtonInterpolator = NewtonInterpolator(xs, ys)
    [print(beautify_decimal(c.quantize(Decimal("0.01"))), end=" ") for c in ni.coefficients]

    plot = Plot(xs[0] - 1, xs[-1] + 1)
    plot.add_equation(ni.interpolate_row, Colour.GREEN, "interpolation")
    plot.add_protected_equation(function.protected_function_row, Colour.BLUE, "original")
    plot.add_points(xs, ys, Colour.YELLOW, Marker.CIRCLE_MARKER)
    plot.show()
