from decimal import DecimalException, Decimal

from base import beautify_decimal
from equations import IntegratorParamSpec, LeftRectangleIntegrator, RightRectangleIntegrator, LambdaEquation
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
        functions.TrigonometricEquation(functions.TrigonometricEquationType.SIN) / functions.LinearEquation(),
        functions.SignEquation(),
    ]

    for equation in equations:
        for integrator in integrators:
            print(beautify_decimal(integrator.solve(equation, IntegratorParamSpec(-3, 10))))
