from __future__ import annotations

from decimal import Decimal
from typing import Protocol


class AnyEquation:
    def function(self, x: Decimal) -> Decimal:
        raise NotImplementedError()

    def derivative(self, x: Decimal) -> Decimal:
        raise NotImplementedError()

    def fixed_point(self, x: Decimal) -> Decimal:
        raise NotImplementedError()

    def __call__(self, other: AnyEquation) -> AnyEquation:
        if not isinstance(other, AnyEquation):
            raise TypeError("")

        return LambdaEquation(lambda x: self.function(other.function(x)),
                              lambda x: self.derivative(other.function(x)) * other.derivative(x))

    def __pos__(self):
        return LambdaEquation(self.function, self.derivative, self.fixed_point)

    def __neg__(self):
        return LambdaEquation(lambda x: -self.function(x), lambda x: -self.derivative(x), self.fixed_point)

    def __add__(self, other: Decimal | AnyEquation):
        if isinstance(other, Decimal):
            return LambdaEquation(lambda x: self.function(x) + other, self.derivative)
        if isinstance(other, AnyEquation):
            return LambdaEquation(lambda x: self.function(x) + other.function(other),
                                  lambda x: self.derivative(x) + other.derivative(x))
        raise TypeError("")

    def __sub__(self, other: Decimal | AnyEquation):
        if isinstance(other, Decimal):
            return LambdaEquation(lambda x: self.function(x) - other, self.derivative)
        if isinstance(other, AnyEquation):
            return LambdaEquation(lambda x: self.function(x) - other.function(other),
                                  lambda x: self.derivative(x) - other.derivative(x))
        raise TypeError("")

    def __mul__(self, other: Decimal | AnyEquation):
        if isinstance(other, Decimal):
            return LambdaEquation(
                lambda x: self.function(x) * other, lambda x: self.derivative(x) * other, self.fixed_point)
        if isinstance(other, AnyEquation):
            def derivative(x: Decimal) -> Decimal:
                return self.derivative(x) * other.function(x) + self.function(x) * other.derivative(x)

            return LambdaEquation(lambda x: self.function(x) * other.function(other), derivative)
        raise TypeError("")

    def __truediv__(self, other: Decimal | AnyEquation):
        if isinstance(other, Decimal):
            return self * (1 / other)
        if isinstance(other, AnyEquation):
            def derivative(x: Decimal) -> Decimal:
                other_function = other.function(x)
                result: Decimal = self.derivative(x) * other_function - self.function(x) * other.derivative(x)
                return result / other_function ** 2

            return LambdaEquation(lambda x: self.function(x) * other.function(other), derivative)
        raise TypeError("")


class SimpleFunction(Protocol):
    def __call__(self, x: Decimal) -> Decimal:
        pass


class LambdaEquation(AnyEquation):
    def __init__(self, function: SimpleFunction, derivative: SimpleFunction = None,
                 fixed_point: SimpleFunction = None, *, precision: int = 10):
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
