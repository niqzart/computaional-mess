from decimal import Decimal

from base import beautify_decimal, Row
from equations import BisectionSolver, SecantSolver, NewtonSolver, IterationSolver
from equations import StraightParamSpec, IterativeParamSpec, LambdaEquation, EquationSystem

if __name__ == "__main__":
    equation_system = EquationSystem(
        lambda x: Decimal("0.1") * x[0] ** 2 + x[0] + Decimal("0.2") * x[1] ** 2 - Decimal("0.3"),
        lambda x: Decimal("0.2") * x[0] ** 2 + x[1] - Decimal("0.1") * x[0] * x[1] - Decimal("0.7")
    )

    print(equation_system.solve(Row([0.25, 0.75])))

    exit(0)

    e1 = LambdaEquation(
        lambda x: x ** 3 + x ** 2 + Decimal(1),
        lambda x: 3 * x ** 2 + 2 * x,
        lambda x: Decimal(-1) / (x + 1).sqrt(),
    )

    e2 = LambdaEquation(
        lambda x: x + x ** 2,
        lambda x: 1 + 2 * x,
        lambda x: -x ** 2,
    )

    bisection_solver = BisectionSolver()
    secant_solver = SecantSolver()
    newton_solver = NewtonSolver()
    iteration_solver = IterationSolver()

    results_1 = [
        bisection_solver.solve(e1, StraightParamSpec(Decimal(-10), Decimal(10))),
        secant_solver.solve(e1, StraightParamSpec(Decimal(-10), Decimal(10))),
        newton_solver.solve(e1, IterativeParamSpec(Decimal(10))),
    ]

    results_2 = [
        bisection_solver.solve(e2, StraightParamSpec(Decimal("-0.5"), Decimal("0.5"))),
        secant_solver.solve(e2, StraightParamSpec(Decimal("-0.5"), Decimal("0.5"))),
        newton_solver.solve(e2, IterativeParamSpec(Decimal("0.5"))),
        iteration_solver.solve(e2, IterativeParamSpec(Decimal("-0.5"))),
    ]

    for result in results_1:
        print(beautify_decimal(result), beautify_decimal(e1.function(result)))
    for result in results_2:
        print(beautify_decimal(result), beautify_decimal(e2.function(result)))
