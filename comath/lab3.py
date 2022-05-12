from base import beautify_decimal
from equations import IntegratorParamSpec, LeftRectangleIntegrator, RightRectangleIntegrator
from equations import MiddleRectangleIntegrator, TrapezoidalIntegrator, SimpsonsIntegrator
from equations import functions

if __name__ == "__main__":
    e1 = functions.TrigonometricEquation(functions.TrigonometricEquationType.SIN) / functions.LinearEquation()

    integrator1 = LeftRectangleIntegrator()
    integrator2 = RightRectangleIntegrator()
    integrator3 = MiddleRectangleIntegrator()
    integrator4 = TrapezoidalIntegrator()
    integrator5 = SimpsonsIntegrator()

    print(beautify_decimal(integrator1.solve(e1, IntegratorParamSpec(-10, 10))))
    print(beautify_decimal(integrator2.solve(e1, IntegratorParamSpec(-10, 10))))
    print(beautify_decimal(integrator3.solve(e1, IntegratorParamSpec(-10, 10))))
    print(beautify_decimal(integrator4.solve(e1, IntegratorParamSpec(-10, 10))))
    print(beautify_decimal(integrator5.solve(e1, IntegratorParamSpec(-10, 10))))
