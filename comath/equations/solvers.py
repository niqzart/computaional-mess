from abc import ABC
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
    def solve(self, equation: AnyEquation, params: ParamSpec) -> Decimal:
        raise NotImplementedError()


class DifferentialSolver(Solver, ABC):
    def __init__(self, max_steps: int = None, root_precision: int = 20):
        self.max_steps: int | None = max_steps
        self.precision: Decimal = Decimal(f"1E-{root_precision}")

    def is_root(self, y: Decimal) -> bool:
        return abs(y) < self.precision


@dataclass()
class StraightParamSpec(ParamSpec):
    right_limit: NUMBER
    left_limit: NUMBER

    def convert(self) -> tuple[Decimal, Decimal]:
        right, left = map(number_to_decimal, (self.right_limit, self.left_limit))
        return right, left


class StraightSolverABS(DifferentialSolver):
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

        step: int = 0
        xi = self._solve(equation, a, f_a, b, f_b)
        f_xi: Decimal = equation.function(xi)
        while not self.is_root(f_xi) and (self.max_steps is None or step < self.max_steps):
            if f_a.is_signed() != f_xi.is_signed():
                b, f_b = xi, f_xi
            else:
                a, f_a = xi, f_xi
            xi = self._solve(equation, a, f_a, b, f_b)
            f_xi: Decimal = equation.function(xi)
            step += 1
        return xi


class BisectionSolver(StraightSolverABS):
    def _solve(self, equation: AnyEquation, a: Decimal, f_a: Decimal, b: Decimal, f_b: Decimal) -> Decimal:
        return (a + b) / 2


class SecantSolver(StraightSolverABS):
    def _solve(self, equation: AnyEquation, a: Decimal, f_a: Decimal, b: Decimal, f_b: Decimal) -> Decimal:
        return a - (f_a * (b - a)) / (f_b - f_a)


@dataclass()
class IterativeParamSpec(ParamSpec):
    initial_guess: NUMBER

    def convert(self) -> Decimal:
        return number_to_decimal(self.initial_guess)


class IterativeSolverABS(DifferentialSolver):
    def _solve(self, equation: AnyEquation, x_n: Decimal, f_x_n: Decimal) -> Decimal:
        raise NotImplementedError()

    def solve(self, equation: AnyEquation, params: IterativeParamSpec) -> Decimal:
        step: int = 0
        x_n = params.convert()
        f_n = equation.function(x_n)
        while not self.is_root(f_n) and (self.max_steps is None or step < self.max_steps):
            x_n = self._solve(equation, x_n, f_n)
            f_n = equation.function(x_n)
            step += 1
        return x_n


class NewtonSolver(IterativeSolverABS):
    def _solve(self, equation: AnyEquation, x_n: Decimal, f_n: Decimal) -> Decimal:
        return x_n - f_n / equation.derivative(x_n)


class IterationSolver(IterativeSolverABS):
    def _solve(self, equation: AnyEquation, x_n: Decimal, f_n: Decimal) -> Decimal:
        if equation.fixed_point is None:
            raise ValueError("")
        return equation.fixed_point(x_n)  # noqa
