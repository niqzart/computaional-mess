from decimal import Decimal, DecimalException
from enum import Enum
from typing import Callable

from base import beautify_decimal, Row, input_decimal, input_menu, checked_input, input_int_range
from equations import BisectionSolver, SecantSolver, NewtonSolver, IterationSolver, functions, AnyEquation, Solver
from equations import StraightParamSpec, IterativeParamSpec, LambdaEquation, EquationSystem


class ExampleFunction(Enum):
    SQUARE_FUNCTION = "Square function: ax² + bx + c"
    POLYNOMIAL_FUNCTION = "Polynomial function: ∑(aₖ xᵏ) for k ∈ [0, n]"


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
    solver_types = [
        BisectionSolver,
        SecantSolver,
        NewtonSolver,
        IterationSolver,
    ]

    while True:
        precision = input_int_range("Enter the i to set the expected precision as 10⁻ⁱ: ", 1, 20)

        solvers: dict[str, Solver] = {solver_type.__name__: solver_type(root_precision=precision, max_steps=1000000)
                                      for solver_type in solver_types}

        function: AnyEquation
        antiderivative: Callable[[Decimal], Decimal]
        has_breaks: bool = False

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

        print("\nEntering params for BisectionSolver and SecantSolver")
        left: Decimal = input_decimal("Enter the left border: ")
        right: Decimal = input_decimal("Enter the right border: ", lambda x: x if x > left else None)

        print("\nEntering the params for NewtonSolver and IterationSolver")
        initial_guess: Decimal = input_decimal("Enter the initial guess: ")

        params_straight: StraightParamSpec = StraightParamSpec(left, right)
        params_iterative: IterativeParamSpec = IterativeParamSpec(initial_guess)

        results: dict[str, Decimal | None] = {}
        for i, (name, solver) in enumerate(solvers.items()):
            try:
                results[name] = solver.solve(function, params_straight if i < 2 else params_iterative)
            except ValueError as e:
                print(f"ERROR for {name}:", e.args[0])
                results[name] = None
            except DecimalException as e:
                print(f"ERROR for {name}:", e.args[0][0].__name__)
                results[name] = None

        print("\nResults:")
        for name, result in results.items():
            if result is not None:
                print(f"{name + ':':30} {beautify_decimal(result):30}")
        break

    equation_system1 = EquationSystem(
        lambda x: Decimal("0.1") * x[0] ** 2 + x[0] + Decimal("0.2") * x[1] ** 2 - Decimal("0.3"),
        lambda x: Decimal("0.2") * x[0] ** 2 + x[1] - Decimal("0.1") * x[0] * x[1] - Decimal("0.7")
    )

    equation_system2 = EquationSystem(
        lambda x: x[0] ** 2 + x[1] ** 2 + x[2] ** 2 - Decimal("16"),
        lambda x: x[0] + x[1] + x[2] - Decimal(2),
        lambda x: x[0] - x[1] - x[2] - Decimal(2),
    )

    print(equation_system1.solve(Row([0.25, 0.75])))
    print(equation_system2.solve(Row([0.25, -0.5, 0.75])))
    print(equation_system2.solve(Row([-0.25, 0.5, -0.75])))

    e1 = LambdaEquation(
        lambda x: x ** 3 + x ** 2 + Decimal(1),
        lambda x: 3 * x ** 2 + 2 * x,
        lambda x: Decimal(-1) / (x + 1).sqrt(),
    )
