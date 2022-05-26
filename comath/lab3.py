from decimal import Decimal, DecimalException
from enum import Enum
from typing import Callable

from base import beautify_decimal, input_menu, input_decimal, checked_input, input_bool, input_int_range
from equations import IntegratorParamSpec, LeftRectangleIntegrator, RightRectangleIntegrator, AnyEquation, Integrator
from equations import MiddleRectangleIntegrator, TrapezoidalIntegrator, SimpsonsIntegrator
from equations import functions

HIDE_SEPARATIONS: bool = False


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
    return lambda x: abs(k * x + b).ln() / k


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
        result += base ** k / (k * step)
        step *= fact * (fact + 1)
        fact += 2

    result *= Decimal("-0.5")
    result += x * functions.TrigonometricEquation(functions.TrigonometricEquationType.SIN).function(1 / x)
    result += -EULER_MASCHERONI + x.ln()
    return result


Empty = object()


def precision_or_none_check(line: str) -> int | object | None:
    try:
        if line.strip() == "":
            return Empty
        result = int(line)
        if 0 < result <= 10:
            return result
        return None
    except ValueError:
        return None


if __name__ == "__main__":
    integrator_types = [
        LeftRectangleIntegrator,
        RightRectangleIntegrator,
        MiddleRectangleIntegrator,
        TrapezoidalIntegrator,
        SimpsonsIntegrator,
    ]

    while True:
        digits: int = checked_input("Enter the precision power (1E-<input>) or press Enter to skip: ",
                                    precision_or_none_check)
        by_precision = digits is not Empty
        if by_precision:
            precision: Decimal = Decimal(f"1E-{digits + 1}")

        function: AnyEquation
        antiderivative: Callable[[Decimal], Decimal]
        has_breaks: bool = False
        second_breaks: list[Decimal] = []

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
                second_breaks.append(-b)
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
                second_breaks.append(Decimal())
                has_breaks = True  # noqa

        left: Decimal = input_decimal("Enter the left border: ")
        right: Decimal = input_decimal("Enter the right border: ", lambda x: x if x > left else None)

        if any(left <= sb <= right for sb in second_breaks):
            print("There are second-type break(s) in this range for this function")
            print("The integral does not converge", end="\n\n")
            continue

        results: dict[str, tuple[Decimal, int | None]]
        if by_precision:
            print("\nCalculating the results...")
            integrator = TrapezoidalIntegrator(10)
            prev: Decimal = integrator.solve(function, IntegratorParamSpec(left, right))
            curr: Decimal
            while True:
                integrator.separations *= 2
                curr = integrator.solve(function, IntegratorParamSpec(left, right))
                if abs(curr - prev) <= precision:
                    break
                prev = curr
            results = {TrapezoidalIntegrator.__name__: (curr, integrator.separations)}
        else:
            integrators: dict[str, Integrator] = {integrator_type.__name__: integrator_type()
                                                  for integrator_type in integrator_types}
            print("\nCalculating the results...")
            if has_breaks:
                print("Algorithmic mean will be used to deal with breaks")
            results = {name: (integrator.solve(function, IntegratorParamSpec(left, right)), integrator.separations)
                       for name, integrator in integrators.items()}

        results["NewtonLeibnizRule"] = (antiderivative(right) - antiderivative(left), None)

        print("\nResults:")
        for name, (result, separations) in results.items():
            sep_description = () if HIDE_SEPARATIONS or separations is None else ("done in", separations, "separations")
            print(f"{name + ':':30} {beautify_decimal(result):30}", *sep_description)

        if not input_bool("\nDo you want to continue integrating? "):
            break
        print()
