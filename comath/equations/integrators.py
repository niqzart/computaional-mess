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
    def __init__(self, separations: int = 1000000):
        self.separations = separations

    def _solve(self, equation: AnyEquation, a: Decimal, b: Decimal) -> Decimal:
        raise NotImplementedError()

    def solve(self, equation: AnyEquation, params: IntegratorParamSpec) -> Decimal:
        a, b = params.convert()
        # result: Decimal = Decimal()
        # for i in range(self.separations - 1):
        #     result +=
        return self._solve(equation, a, b)


class LeftRectangleIntegrator(Integrator):
    def _solve(self, equation: AnyEquation, a: Decimal, b: Decimal) -> Decimal:
        result: Decimal = Decimal()
        step_size: Decimal = (b - a) / self.separations
        step_start: Decimal = a
        for _ in range(self.separations - 1):
            result += equation.function(step_start) * step_size
            step_start += step_size
        return result


class RightRectangleIntegrator(Integrator):
    def _solve(self, equation: AnyEquation, a: Decimal, b: Decimal) -> Decimal:
        result: Decimal = Decimal()
        step_size: Decimal = (b - a) / self.separations
        step_start: Decimal = a + step_size
        for _ in range(self.separations - 1):
            result += equation.function(step_start) * step_size
            step_start += step_size
        return result


class MiddleRectangleIntegrator(Integrator):
    def _solve(self, equation: AnyEquation, a: Decimal, b: Decimal) -> Decimal:
        result: Decimal = Decimal()
        step_size: Decimal = (b - a) / self.separations
        step_start: Decimal = a + step_size / 2
        for _ in range(self.separations - 1):
            result += equation.function(step_start) * step_size
            step_start += step_size
        return result


class TrapezoidalIntegrator(Integrator):
    def _solve(self, equation: AnyEquation, a: Decimal, b: Decimal) -> Decimal:
        result: Decimal = Decimal()
        step_size: Decimal = (b - a) / self.separations
        step_start: Decimal = a
        function_start: Decimal = equation.function(step_start)
        function_next: Decimal
        for _ in range(self.separations):
            step_start += step_size
            function_next = equation.function(step_start)
            result += (function_start + function_next) * step_size / 2
            function_start = function_next
        return result


class SimpsonsIntegrator(Integrator):
    def _solve(self, equation: AnyEquation, a: Decimal, b: Decimal) -> Decimal:
        result: Decimal = Decimal()
        step_size: Decimal = (b - a) / self.separations
        step_start: Decimal = a
        function_start: Decimal = equation.function(step_start)
        function_next: Decimal
        for _ in range(self.separations):
            step_start += step_size / 2
            function_mid = equation.function(step_start)
            step_start += step_size / 2
            function_next = equation.function(step_start)
            result += (function_start + 4 * function_mid + function_next) * step_size / 6
            function_start = function_next
        return result
