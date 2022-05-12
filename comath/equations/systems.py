from decimal import Decimal
from typing import Protocol


class FunctionProtocol(Protocol):
    def __call__(self, *args: Decimal) -> Decimal:
        pass


class DerivativeProtocol(Protocol):
    def __call__(self, *args: Decimal, derive_by: int = 0) -> Decimal:
        pass


class MultiEquation:
    def __init__(self, function: FunctionProtocol, derivative: DerivativeProtocol = None, *, precision: int = 10):
        self.function: FunctionProtocol = function
        if derivative is not None:
            self.derivative: DerivativeProtocol = derivative
        self.precision: Decimal = Decimal(f"1E-{precision}")

    def derivative(self, *args: Decimal, derive_by: int = 0) -> Decimal:
        args_moved = list(args)
        args_moved[derive_by] += self.precision
        return (self.function(*args_moved) - self.function(*args)) / self.precision


class EquationSystem:
    def __init__(self, *equations: FunctionProtocol | tuple[FunctionProtocol, DerivativeProtocol], precision: int = 10):
        self.equations: list[MultiEquation] = [MultiEquation(*equation, precision=precision) for equation in equations]

    def __iter__(self):
        return self.equations

    def __getitem__(self, item):
        return self.equations.__getitem__(item)
