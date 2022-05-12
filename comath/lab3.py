from decimal import Decimal

from base import beautify_decimal
from equations import IntegratorParamSpec, LeftRectangleIntegrator, RightRectangleIntegrator
from equations import MiddleRectangleIntegrator, TrapezoidalIntegrator, SimpsonsIntegrator
from equations import functions

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
