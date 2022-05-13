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
    integrators = [
        LeftRectangleIntegrator(),
        RightRectangleIntegrator(),
        MiddleRectangleIntegrator(),
        TrapezoidalIntegrator(),
        SimpsonsIntegrator(),
    ]

    equations = [
        functions.SquareEquation(),
        functions.TrigonometricEquation(functions.TrigonometricEquationType.SIN) / functions.LinearEquation(),
        functions.SignEquation(),
        Decimal(1) / functions.LinearEquation(),
        functions.TrigonometricEquation(functions.TrigonometricEquationType.SIN)(
            Decimal(1) / functions.LinearEquation()),
        functions.PolynomialEquation(1, -2, 3, -4, 5, -6)
    ]

    for equation in equations:
        for integrator in integrators:
            print(beautify_decimal(integrator.solve(equation, IntegratorParamSpec(-3, 10))))
        print()
