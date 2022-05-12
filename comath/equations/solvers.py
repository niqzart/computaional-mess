from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from base import NUMBER, number_to_decimal
from equations import AnyEquation


class SolveMethod(Enum):
    BISECTION = "Bisection method"
    SECANT = "Secant method"
    NEWTON = "Newton's (tangent) method"
    ITERATION = "Fixed-point iteration method"


class ParamSpec:
    def convert(self) -> ...:
        raise NotImplementedError()


class Solver:
    def __init__(self, root_precision: int = 10):
        self.precision: Decimal = Decimal(f"1E-{root_precision}")

    def is_root(self, y: Decimal) -> bool:
        return abs(y) < self.precision

    def solve(self, equation: AnyEquation, params: ParamSpec) -> Decimal:
        raise NotImplementedError()


@dataclass()
class StraightParamSpec(ParamSpec):
    right_limit: NUMBER
    left_limit: NUMBER

    def convert(self) -> tuple[Decimal, Decimal]:
        right, left = map(number_to_decimal, (self.right_limit, self.left_limit))
        return right, left


class StraightSolverABS(Solver):
    def _solve(self, equation: AnyEquation, a: Decimal, f_a: Decimal, b: Decimal, f_b: Decimal) -> Decimal:
        raise NotImplementedError()

    def solve(self, equation: AnyEquation, params: StraightParamSpec) -> Decimal:
        a, b = params.convert()
        f_a: Decimal = equation.function(a)
        f_b: Decimal = equation.function(b)
        if f_a == 0:
            return a
        if f_b == 0:
            return b
        if f_a * f_b > 0:
            raise ValueError("")
        return self._solve(equation, a, f_a, b, f_b)


class BisectionSolver(StraightSolverABS):
    def _solve(self, equation: AnyEquation, a: Decimal, f_a: Decimal, b: Decimal, f_b: Decimal) -> Decimal:
        xi = (a + b) / 2
        f_xi: Decimal = equation.function(xi)
        if self.is_root(f_xi):
            return xi
        if f_a.is_signed() != f_xi.is_signed():
            return self._solve(equation, a, f_a, xi, f_xi)
        return self._solve(equation, xi, f_xi, b, f_b)


class SecantSolver(StraightSolverABS):
    def _solve(self, equation: AnyEquation, a: Decimal, f_a: Decimal, b: Decimal, f_b: Decimal) -> Decimal:
        xi = a - (f_a * (b - a)) / (f_b - f_a)
        f_xi: Decimal = equation.function(xi)
        if self.is_root(f_xi):
            return xi
        if f_a.is_signed() != f_xi.is_signed():
            return self._solve(equation, a, f_a, xi, f_xi)
        return self._solve(equation, xi, f_xi, b, f_b)


@dataclass()
class IterativeParamSpec(ParamSpec):
    initial_guess: NUMBER

    def convert(self) -> Decimal:
        return number_to_decimal(self.initial_guess)


class IterativeSolverABS(Solver):
    def _solve(self, equation: AnyEquation, x_n: Decimal, f_x_n: Decimal) -> Decimal:
        raise NotImplementedError()

    def solve(self, equation: AnyEquation, params: IterativeParamSpec) -> Decimal:
        x_n = params.convert()
        f_x_n = equation.function(x_n)
        return self._solve(equation, x_n, f_x_n)


class NewtonSolver(IterativeSolverABS):
    def _solve(self, equation: AnyEquation, x_n: Decimal, f_x_n: Decimal):
        x_n1 = x_n - f_x_n / equation.derivative(x_n)
        f_x_n1 = equation.function(x_n1)
        if self.is_root(f_x_n1):
            return x_n1
        return self._solve(equation, x_n1, f_x_n1)


class IterationSolver(IterativeSolverABS):
    def _solve(self, equation: AnyEquation, x_n: Decimal, _) -> Decimal:
        if equation.fixed_point is None:
            raise ValueError("")
        x_n1 = equation.fixed_point(x_n)  # noqa
        f_x_n1 = equation.function(x_n1)
        if self.is_root(f_x_n1):
            return x_n1
        return self._solve(equation, x_n1, f_x_n1)
