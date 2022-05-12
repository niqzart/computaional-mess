from decimal import Decimal

from base import beautify_decimal
from equations import LambdaEquation, IntegratorParamSpec, LeftRectangleIntegrator, RightRectangleIntegrator
from equations import MiddleRectangleIntegrator, TrapezoidalIntegrator, SimpsonsIntegrator

if __name__ == "__main__":
    e1 = LambdaEquation(
        lambda x: x ** 3 / 3,
        lambda x: x ** 2,
    )

    integrator1 = LeftRectangleIntegrator()
    integrator2 = RightRectangleIntegrator()
    integrator3 = MiddleRectangleIntegrator()
    integrator4 = TrapezoidalIntegrator()
    integrator5 = SimpsonsIntegrator()

    print(beautify_decimal(integrator1.solve(~e1, IntegratorParamSpec(-3, 10))))
    print(beautify_decimal(integrator2.solve(~e1, IntegratorParamSpec(-3, 10))))
    print(beautify_decimal(integrator3.solve(~e1, IntegratorParamSpec(-3, 10))))
    print(beautify_decimal(integrator4.solve(~e1, IntegratorParamSpec(-3, 10))))
    print(beautify_decimal(integrator5.solve(~e1, IntegratorParamSpec(-3, 10))))
