from dataclasses import dataclass
from decimal import Decimal, DecimalException

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
    default_steps = 10000

    def __init__(self, separations: int = None, root_precision: int = None):
        super().__init__(root_precision)
        self.separations = separations or self.default_steps

    def _function_or_break(self, equation: AnyEquation, x: Decimal) -> Decimal:
        try:
            return equation.function(x)
        except DecimalException:
            return (equation.function(x - self.precision) + equation.function(x + self.precision)) / 2

    def _solve(self, equation: AnyEquation, a: Decimal, b: Decimal, step_size: Decimal) -> Decimal:
        raise NotImplementedError()

    def solve(self, equation: AnyEquation, params: IntegratorParamSpec) -> Decimal:
        a, b = params.convert()
        step_size: Decimal = (b - a) / self.separations
        # result: Decimal = Decimal()
        # for i in range(self.separations - 1):
        #     result +=
        return self._solve(equation, a, b, step_size)


class RectangleIntegratorABS(Integrator):
    default_steps = 1000000

    def _step_start(self, a: Decimal, step_size: Decimal):
        raise NotImplementedError()

    def _solve(self, equation: AnyEquation, a: Decimal, b: Decimal, step_size: Decimal) -> Decimal:
        result: Decimal = Decimal()
        step_start: Decimal = self._step_start(a, step_size)
        for _ in range(self.separations - 1):
            result += self._function_or_break(equation, step_start) * step_size
            step_start += step_size
        return result


class RightRectangleIntegrator(RectangleIntegratorABS):
    default_steps = 1000000

    def _step_start(self, a: Decimal, step_size: Decimal):
        return a


class MiddleRectangleIntegrator(RectangleIntegratorABS):
    def _step_start(self, a: Decimal, step_size: Decimal):
        return a + step_size / 2


class LeftRectangleIntegrator(RectangleIntegratorABS):
    default_steps = 1000000

    def _step_start(self, a: Decimal, step_size: Decimal):
        return a + step_size


class ComplexIntegratorABS(Integrator):
    def _calc_step(self, f_start: Decimal, f_mid: Decimal, f_next: Decimal, half_step_size: Decimal):
        raise NotImplementedError()

    def _solve(self, equation: AnyEquation, a: Decimal, b: Decimal, step_size: Decimal) -> Decimal:
        result: Decimal = Decimal()
        step_size /= 2
        step_start: Decimal = a
        function_start: Decimal = self._function_or_break(equation, step_start)
        function_next: Decimal
        for _ in range(self.separations):
            step_start += step_size
            function_mid = self._function_or_break(equation, step_start)
            step_start += step_size
            function_next = self._function_or_break(equation, step_start)
            result += self._calc_step(function_start, function_mid, function_next, step_size)
            function_start = function_next
        return result


class TrapezoidalIntegrator(ComplexIntegratorABS):
    default_steps = 10000

    def _calc_step(self, f_start: Decimal, f_mid: Decimal, f_next: Decimal, half_step_size: Decimal):
        return (f_start + f_next) * half_step_size


class SimpsonsIntegrator(ComplexIntegratorABS):
    default_steps = 100

    def _calc_step(self, f_start: Decimal, f_mid: Decimal, f_next: Decimal, half_step_size: Decimal):
        return (f_start + 4 * f_mid + f_next) * half_step_size / 3
