from __future__ import annotations

from decimal import Decimal
from typing import Protocol


class AnyEquation:
    def function(self, x: Decimal) -> Decimal:
        raise NotImplementedError()

    def __call__(self, x: Decimal) -> Decimal:
        return self.function(x)

    def derivative(self, x: Decimal) -> Decimal:
        raise NotImplementedError()

    def fixed_point(self, x: Decimal) -> Decimal:
        raise NotImplementedError()


class SimpleFunction(Protocol):
    def __call__(self, x: Decimal) -> Decimal:
        pass


class LambdaEquation(AnyEquation):
    def __init__(self, function: SimpleFunction, fixed_point: SimpleFunction = None,
                 derivative: SimpleFunction = None, *, precision: int = 10):
        self.function: SimpleFunction = function
        self.fixed_point: SimpleFunction | None = fixed_point
        if derivative is not None:
            self.derivative: SimpleFunction = derivative
        self.precision: Decimal = Decimal(f"1E-{precision}")

    def function(self, x: Decimal) -> Decimal:
        pass

    def derivative(self, x: Decimal) -> Decimal:
        return (self.function(x + self.precision) - self.function(x)) / self.precision

    def fixed_point(self, x: Decimal) -> Decimal:
        pass
