from decimal import Decimal
from typing import Protocol

from base import Row, LinearEquationSystem


class FunctionProtocol(Protocol):
    def __call__(self, x: Row) -> Decimal:
        pass


class DerivativeProtocol(Protocol):
    def __call__(self, x: Row, derive_by: int = 0) -> Decimal:
        pass


class MultiEquation:
    def __init__(self, function: FunctionProtocol, derivative: DerivativeProtocol = None, *, precision: int = 10):
        self.function: FunctionProtocol = function
        if derivative is not None:
            self.derivative: DerivativeProtocol = derivative
        self.precision: Decimal = Decimal(f"1E-{precision}")

    def derivative(self, x: Row, derive_by: int = 0) -> Decimal:
        x_moved: Row = x.copy()
        x_moved[derive_by] += self.precision
        return (self.function(x_moved) - self.function(x)) / self.precision


class EquationSystem:
    @staticmethod
    def _unpack_equation(equation: FunctionProtocol | tuple[FunctionProtocol, DerivativeProtocol]) -> tuple:
        if isinstance(equation, tuple):
            return equation
        return tuple([equation])

    def __init__(self, *equations: FunctionProtocol | tuple[FunctionProtocol, DerivativeProtocol],
                 precision: int = 10, max_steps: int = 10000):
        self.equations: list[MultiEquation] = [MultiEquation(*self._unpack_equation(equation), precision=precision)
                                               for equation in equations]
        self.precision: Decimal = Decimal(f"1E-{precision}")
        self.max_steps: int = max_steps

    def __len__(self):
        return len(self.equations)

    def __iter__(self):
        return self.equations.__iter__()

    def __getitem__(self, item):
        return self.equations.__getitem__(item)

    def solve(self, x: Row):
        step = 0
        delta_x: Row | None = None
        while (delta_x is None or abs(max(delta_x)) > self.precision) and step < self.max_steps:
            jacobian = LinearEquationSystem([
                Row([equation.derivative(x, derive_by=i) for i in range(len(self))]
                    + [equation.function(x)])
                for equation in self])
            delta_x = jacobian.solve()[0]
            x -= delta_x
            step += 1
        return x
