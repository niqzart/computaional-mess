from decimal import Decimal, DecimalException
from enum import Enum
from typing import Callable

from base import beautify_decimal, input_menu, input_decimal, checked_input, input_bool, input_int_range
from equations import IntegratorParamSpec, LeftRectangleIntegrator, RightRectangleIntegrator, AnyEquation, Integrator
from equations import MiddleRectangleIntegrator, TrapezoidalIntegrator, SimpsonsIntegrator
from equations import functions


class ExampleFunction(Enum):
    SQUARE_FUNCTION = "Square function: ax² + bx + c"
    POLYNOMIAL_FUNCTION = "Polynomial function: ∑(aₖ xᵏ) for k ∈ [0, n]"
    INVERSE_FUNCTION = "Inverse function: 1 / (kx + b)"
    SIGN_FUNCTION = "Sign function: |x| / x"
    SINC_FUNCTION = "Sinc function: six(x) / x"
    OSCILLATING_FUNCTION = "Oscillating function: sin(1 / x)"


def square_function_antiderivative(a: Decimal, b: Decimal, c: Decimal):
    return lambda x: a * x ** 3 / 3 + b * x ** 2 / 2 + c * x


def coefficients_check(line: str) -> list[Decimal] | None:
    try:
        result = [Decimal(c) for c in line.replace(",", ".").strip().split()]
        return None if result[0] == 0 else result
    except DecimalException:
        return None


def polynomial_function_antiderivative(*coefficients: Decimal):
    def result(x: Decimal) -> Decimal:
        result: Decimal = Decimal()
        n: int = len(coefficients)
        for i, coefficient in enumerate(coefficients):
            result = result * x + coefficient / (n - i)
        return result

    return result


def inverse_function_antiderivative(k: Decimal, b: Decimal):
    return lambda x: (k * x + b).ln() / k


SINC_FUNCTION = functions.TrigonometricEquation(functions.TrigonometricEquationType.SIN) / functions.LinearEquation()


def sinc_function_antiderivative(x: Decimal) -> Decimal:
    result = Decimal()
    step = Decimal(1)
    fact = Decimal(2)
    for k in range(1, 100):
        temp = 2 * k - 1
        temp = x ** temp / (temp * step)
        result += temp if k % 2 == 1 else -temp
        step *= fact * (fact + 1)
        fact += 2
    return result


INVERSE_FUNCTION = Decimal(1) / functions.LinearEquation()
OSCILLATING_FUNCTION = functions.TrigonometricEquation(functions.TrigonometricEquationType.SIN)(INVERSE_FUNCTION)
EULER_MASCHERONI = Decimal("0.57721566490153286060651209008240243104215933593992")


def oscillating_function_antiderivative(x: Decimal) -> Decimal:
    x = abs(x)
    result = Decimal()
    base = -1 / x ** 2
    step = Decimal(2)
    fact = Decimal(3)
    for k in range(1, 100):
        result += base ** k / (2 * k * step)
        step *= fact * (fact + 1)
        fact += 2

    result *= Decimal("-0.5")
    result += x * functions.TrigonometricEquation(functions.TrigonometricEquationType.SIN).function(1 / x)
    result += -EULER_MASCHERONI + x.ln()
    return result


if __name__ == "__main__":
    integrator_types = [
        LeftRectangleIntegrator,
        RightRectangleIntegrator,
        MiddleRectangleIntegrator,
        TrapezoidalIntegrator,
        SimpsonsIntegrator,
    ]

    while True:
        by_max_steps = input_bool("Do you want to specify the amount of steps instead of precision? ")
        print("Interpreting as", "Yes" if by_max_steps else "No")
        if by_max_steps:
            max_steps = input_int_range("Enter the number of steps: ", 1, 1000000000000000)
        else:
            precision = input_decimal("Enter the precision: ", lambda x: x if 0 < x < 1 else None)
            max_steps = None

        integrators: dict[str, Integrator] = {integrator_type.__name__: integrator_type(max_steps)
                                              for integrator_type in integrator_types}

        function: AnyEquation
        antiderivative: Callable[[Decimal], Decimal]
        has_breaks: bool = False

        match input_menu(ExampleFunction, "Enter the function to integrate: "):
            case ExampleFunction.SQUARE_FUNCTION:
                a = input_decimal("Enter a ≠ 0: ", lambda x: None if x == 0 else x)
                b = input_decimal("Enter b: ")
                c = input_decimal("Enter c: ")
                function = functions.SquareEquation(a, b, c)
                antiderivative = square_function_antiderivative(a, b, c)
            case ExampleFunction.POLYNOMIAL_FUNCTION:
                prompt = "Enter all coefficients (space separated, starting with the senior one): "
                coefficients = checked_input(prompt, coefficients_check)
                function = functions.PolynomialEquation(*coefficients)
                antiderivative = polynomial_function_antiderivative(*coefficients)
            case ExampleFunction.INVERSE_FUNCTION:
                k = input_decimal("Enter k ≠ 0: ", lambda x: None if x == 0 else x)
                b = input_decimal("Enter b: ")
                function = Decimal(1) / functions.LinearEquation(k, b)
                antiderivative = inverse_function_antiderivative(k, b)
                has_breaks = True  # noqa
            case ExampleFunction.SIGN_FUNCTION:
                reverse = input_bool("Do you want to reverse the sign function? ")
                print("Interpreting as", "Yes" if reverse else "No")
                function = functions.SignEquation(reverse)
                antiderivative = abs
                has_breaks = True  # noqa
            case ExampleFunction.SINC_FUNCTION:
                function = SINC_FUNCTION
                antiderivative = sinc_function_antiderivative
                has_breaks = True  # noqa
            case ExampleFunction.OSCILLATING_FUNCTION:
                function = OSCILLATING_FUNCTION
                antiderivative = oscillating_function_antiderivative
                has_breaks = True  # noqa

        left: Decimal = input_decimal("Enter the left border: ")
        right: Decimal = input_decimal("Enter the right border: ", lambda x: x if x > left else None)

        print("\nCalculating the results...")
        if has_breaks:
            print("Algorithmic mean will be used to deal with breaks")

        results: dict[str, tuple[Decimal, int | None]] = {
            name: (integrator.solve(function, IntegratorParamSpec(left, right)), integrator.separations)
            for name, integrator in integrators.items()
        }
        results["NewtonLeibnizRule"] = (antiderivative(right) - antiderivative(left), None)

        print("\nResults:")
        for name, (result, separations) in results.items():
            sep_description = () if separations is None else ("done in", separations, "separations")
            print(f"{name + ':':30} {beautify_decimal(result):30}", *sep_description)

        no_exit = input_bool("Do you want to continue integrating? ")
        if not no_exit:
            break
