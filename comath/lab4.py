from decimal import Decimal, DecimalException, InvalidOperation
from enum import Enum

from base import Row, input_bool, checked_input, input_decimal, input_menu, beautify_decimal, input_int
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


Empty = object()


def decimal_or_empty_check(line: str) -> Decimal | object | None:
    try:
        if line.strip() == "":
            return Empty
        return Decimal(line.replace(",", "."))
    except InvalidOperation:
        return None


SINC_FUNCTION = functions.TrigonometricEquation(functions.TrigonometricEquationType.SIN) / functions.LinearEquation()
INVERSE_FUNCTION = Decimal(1) / functions.LinearEquation()
OSCILLATING_FUNCTION = functions.TrigonometricEquation(functions.TrigonometricEquationType.SIN)(INVERSE_FUNCTION)

if __name__ == "__main__":
    function: AnyEquation

    while True:
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

        if input_bool("\nDo you want to input xs manually? "):
            while True:
                try:
                    xs = Row.from_line(input("Enter coefficients (separate with spaces): ").strip())
                    xs.data = list(set(xs.data))
                    xs.size = len(xs.data)
                    break
                except ValueError as e:
                    print(e.args[0])
        else:
            a = input_int("Enter the interval start (int): ")
            b = input_int("Enter the interval end (int): ", lambda x: x if x > a else None)
            xs = Row([i for i in range(a, b)])

        print()
        ys = function.protected_function_row(xs)
        if ys.count(None) == len(ys):
            print("ERROR: None of the values for inputted Xs are defined\n")
            continue
        if ys.count(None) > 0:
            print("Some function values for some Xs are not defined, they will be skipped")
            xs = Row([xs[i] for i in range(xs.size) if ys[i] is not None])
            ys = Row([y for y in ys if y is not None])
        ys = distort_row(ys, input_int("Enter the distortion coefficient: ", lambda x: x if x >= 0 else None))

        print("Interpolation nodes (x, y):")
        [print(beautify_decimal(xs[i]), beautify_decimal(ys[i])) for i in range(xs.size)]

        ni: NewtonInterpolator = NewtonInterpolator(xs, ys)
        print("Interpolating polynomial's coefficients:")
        print(Row(ni.coefficients))

        plot = Plot(min(xs) - 1, max(xs) + 1)
        plot.add_equation(ni.interpolate_row, Colour.GREEN, "interpolation")
        plot.add_protected_equation(function.protected_function_row, Colour.BLUE, "original")
        plot.add_points(xs, ys, Colour.YELLOW, Marker.CIRCLE_MARKER)
        plot.show()

        if input_bool("\nDo you want to use the interpolator? "):
            while True:
                x = checked_input("Input x (or press Enter nothing to exit): ", decimal_or_empty_check)
                if x is Empty:
                    break
                assert isinstance(x, Decimal)
                yi = ni.interpolate_one(x)
                print("Interpolated y:", beautify_decimal(yi))
                yr = function.protected_function(x)
                if yr is None:
                    print("Real y is not defined")
                else:
                    print("Analytical y:  ", beautify_decimal(yr))
                    print("Error squared: ", beautify_decimal((yi - yr) ** 2))
                print()

        if not input_bool("\nDo you want to continue interpolating? "):
            break
