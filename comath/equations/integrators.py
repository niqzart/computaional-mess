from dataclasses import dataclass
from decimal import Decimal

from base import NUMBER, number_to_decimal
from .functions import AnyEquation
from .solvers import Solver, ParamSpec


@dataclass()
class IntegratorParamSpec(ParamSpec):
    right_limit: NUMBER
    left_limit: NUMBER

    def convert(self) -> tuple[Decimal, Decimal]:
        right, left = map(number_to_decimal, (self.right_limit, self.left_limit))
        return right, left


class Integrator(Solver):
    def __init__(self, separations: int = 10):
        self.separations = separations

    def _solve(self, equation: AnyEquation, a: Decimal, b: Decimal) -> Decimal:
        raise NotImplementedError()

    def solve(self, equation: AnyEquation, params: IntegratorParamSpec) -> Decimal:
        return self._solve(equation, *params.convert())


class RectangleIntegrator(Integrator):
    def _solve(self, equation: AnyEquation, a: Decimal, b: Decimal) -> Decimal:
        pass


class TrapezoidalIntegrator(Integrator):
    def _solve(self, equation: AnyEquation, a: Decimal, b: Decimal) -> Decimal:
        pass


class SimpsonsIntegrator(Integrator):
    def _solve(self, equation: AnyEquation, a: Decimal, b: Decimal) -> Decimal:
        pass
