from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, DecimalException
from enum import Enum
from math import *

from base import NUMBER, number_to_decimal
from equations.interfaces import AnyEquation


@dataclass
class LinearEquation(AnyEquation):
    k: Decimal = Decimal(1)
    b: Decimal = Decimal(0)

    def function(self, x: Decimal) -> Decimal:
        return self.k * x + self.b

    def derivative(self, x: Decimal) -> Decimal:
        return self.k

    def fixed_point(self, x: Decimal) -> Decimal:
        return -self.b / self.k


@dataclass
class SquareEquation(AnyEquation):
    a: Decimal = Decimal(1)
    b: Decimal = Decimal(0)
    c: Decimal = Decimal(0)

    def function(self, x: Decimal) -> Decimal:
        return self.a * x ** 2 + self.b * x + self.c

    def derivative(self, x: Decimal) -> Decimal:
        return self.a * 2 * x + self.b

    def fixed_point(self, x: Decimal) -> Decimal:
        return -self.c / (self.a * x + self.b)


class PolynomialEquation(AnyEquation):
    def __init__(self, *coefficients: NUMBER):
        if len(coefficients) < 3:
            raise ValueError("")
        self.coefficients: tuple[Decimal, ...] = tuple(number_to_decimal(c) for c in coefficients)

    def function(self, x: Decimal) -> Decimal:
        result: Decimal = Decimal()
        for coefficient in self.coefficients:
            result = result * x + coefficient
        return result

    def derivative(self, x: Decimal) -> Decimal:
        result: Decimal = Decimal()
        power: int = len(self.coefficients) - 1
        for coefficient in self.coefficients[:-1]:
            result = result * power * x + coefficient
            power -= 1
        return result

    def fixed_point(self, x: Decimal) -> Decimal:
        result: Decimal = Decimal()
        for coefficient in self.coefficients[:-1]:
            result = result * x + coefficient
        return -self.coefficients[-1] / result


class TrigonometricEquationType(Enum):
    SIN = "Sine"
    COS = "Cosine"
    TAN = "Tangent"
    COT = "Cotangent"
    SEC = "Secant"
    CSC = "Cosecant"

    def apply(self, x: Decimal) -> float:
        match self:
            case TrigonometricEquationType.SIN:
                return sin(x)
            case TrigonometricEquationType.COS:
                return cos(x)
            case TrigonometricEquationType.TAN:
                return tan(x)
            case TrigonometricEquationType.CSC:
                return 1 / sin(x)
            case TrigonometricEquationType.SEC:
                return 1 / cos(x)
            case TrigonometricEquationType.COT:
                return 1 / tan(x)

    def derive(self, x: Decimal) -> float:
        match self:
            case TrigonometricEquationType.SIN:
                return cos(x)
            case TrigonometricEquationType.COS:
                return -sin(x)
            case TrigonometricEquationType.TAN:
                return 1 / cos(x) ** 2
            case TrigonometricEquationType.CSC:
                return -cos(x) / sin(x) ** 2
            case TrigonometricEquationType.SEC:
                return sin(x) / cos(x) ** 2
            case TrigonometricEquationType.COT:
                return -1 / sin(x) ** 2


@dataclass()
class TrigonometricEquation(AnyEquation):
    type: TrigonometricEquationType

    def function(self, x: Decimal) -> Decimal:
        return Decimal.from_float(self.type.apply(x))

    def derivative(self, x: Decimal) -> Decimal:
        return Decimal.from_float(self.type.derive(x))

    fixed_point = None


@dataclass()
class ExponentEquation(AnyEquation):
    a: Decimal | None = None

    def function(self, x: Decimal) -> Decimal:
        if self.a is None:
            return x.exp()
        return self.a ** x

    def derivative(self, x: Decimal) -> Decimal:
        if self.a is None:
            return x.exp()
        return self.a ** x * self.a.ln()

    fixed_point = None


@dataclass()
class LogarithmEquation(AnyEquation):
    a: Decimal | None = None

    def function(self, x: Decimal) -> Decimal:
        if self.a is None:
            return x.ln()
        if self.a == 10:
            return x.log10()
        return Decimal.from_float(log(x, self.a))

    def derivative(self, x: Decimal) -> Decimal:
        if self.a is None:
            return 1 / x
        return 1 / (x * self.a.ln())

    fixed_point = None


@dataclass()
class SignEquation(AnyEquation):
    reversed: bool = False
    zero_as: Decimal | None = None

    def function(self, x: Decimal) -> Decimal:
        if x == 0:
            if self.zero_as is not None:
                return self.zero_as
            raise DecimalException()
        return Decimal(-1 if (x < 0) != self.reversed else 1)

    def derivative(self, x: Decimal) -> Decimal:
        if x == 0:
            raise DecimalException()
        return Decimal()

    fixed_point = None
