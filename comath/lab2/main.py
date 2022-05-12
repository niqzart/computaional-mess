from decimal import Decimal

from base.utils import beautify_decimal
from equations import StraightParamSpec, IterativeParamSpec, LambdaEquation
from equations import BisectionSolver, SecantSolver, NewtonSolver, IterationSolver

if __name__ == "__main__":
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
