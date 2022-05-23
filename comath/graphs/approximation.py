from __future__ import annotations

from decimal import Decimal
from enum import Enum
from math import sin

from base import Row, LinearEquationSystem, NotImplementedField


class ApproximationFunction(Enum):
    CONSTANT = "Constant function: y = a"  # why not?
    LINEAR = "Linear function: y = ax + b"
    LIMITED_SQUARE = "Limited square function: y = ax²"
    FULL_SQUARE = "Square function: y = ax² + bx + c"
    LOGARITHMIC = "Logarithmic function: y = a + b ln(x)"
    TRIGONOMETRIC = "Trigonometric function: y = a sin(x) + b"

    def approximator(self) -> Approximator:
        match self:
            case ApproximationFunction.CONSTANT:
                return ConstantApproximator()
            case ApproximationFunction.LINEAR:
                return LinearApproximator()
            case ApproximationFunction.LIMITED_SQUARE:
                return LimitedSquareApproximator()
            case ApproximationFunction.FULL_SQUARE:
                return SquareApproximator()
            case ApproximationFunction.LOGARITHMIC:
                return LogarithmicApproximator()
            case ApproximationFunction.TRIGONOMETRIC:
                return TrigonometricApproximator()


class Approximator:
    size: int = NotImplementedField

    def __init__(self):
        self.coefficients: Row | None = None

    def prepare(self, xs: Row) -> Row:
        return xs.copy()

    def derivatives(self, xi: Decimal) -> Row:
        raise NotImplementedError()

    def _fit(self, xs: Row, ys: Row):
        es = LinearEquationSystem.from_lambda((self.size, self.size + 1), lambda *_: Decimal())
        for i in range(xs.size):
            xi, yi = xs[i], ys[i]
            derivatives = self.derivatives(xi)
            for k in range(self.size):
                for q in range(self.size):
                    es[k][q] += derivatives[k] * derivatives[q]
                es[k][-1] += derivatives[k] * yi

        self.coefficients = es.solve()[0]

    def fit(self, xs: Row, ys: Row):
        if xs.size != ys.size:
            raise ValueError(f"Xs and Ys side mismatch: {xs.size} != {ys.size}")
        xs = self.prepare(xs)
        return self.fit(xs, ys)

    def predict_one(self, xi: Decimal) -> Decimal:
        raise NotImplementedError()

    def _predict_row(self, xs: Row) -> Row:
        return Row([self.predict_one(x) for x in xs])

    def predict_row(self, xs: Row) -> Row:
        if self.coefficients is None:
            raise ValueError("Approximator is not fitted yet")
        xs = self.prepare(xs)
        return self._predict_row(xs)

    def _calculate_errors(self, predicted: Row, ys: Row) -> Row:
        return Row([(predicted[i] - ys[i]) ** 2 for i in range(predicted.size)])

    def calculate_errors(self, xs: Row, ys: Row) -> Row:
        return self._calculate_errors(self.predict_row(xs), ys)

    def _exclude(self, xs: Row, ys: Row) -> int:
        predicted = self._predict_row(xs)
        return max(((predicted[i] - ys[i]) ** 2, i) for i in range(xs.size))[1]

    def fit_and_exclude(self, xs: Row, ys: Row) -> tuple[int, Row]:
        xs = self.prepare(xs)
        ys = ys.copy()
        self._fit(xs, ys)
        i = self._exclude(xs, ys)
        xs.pop(i)
        ys.pop(i)
        self._fit(xs, ys)
        return i, self._calculate_errors(self._predict_row(xs), ys)


class ConstantApproximator(Approximator):
    size = 1

    def derivatives(self, xi: Decimal) -> Row:
        return Row([Decimal(1)])

    def predict_one(self, xi: Decimal) -> Decimal:
        return self.coefficients[0]


class LinearApproximator(Approximator):
    size = 2

    def derivatives(self, xi: Decimal) -> Row:
        return Row([xi, Decimal(1)])

    def predict_one(self, xi: Decimal) -> Decimal:
        return self.coefficients[0] * xi + self.coefficients[1]


class LimitedSquareApproximator(Approximator):
    size = 1

    def derivatives(self, xi: Decimal) -> Row:
        return Row([xi ** 2])

    def predict_one(self, xi: Decimal) -> Decimal:
        return self.coefficients[0] * xi ** 2


class SquareApproximator(Approximator):
    size = 3

    def derivatives(self, xi: Decimal) -> Row:
        return Row([xi ** 2, xi, Decimal(1)])

    def predict_one(self, xi: Decimal) -> Decimal:
        return self.coefficients[0] * xi ** 2 + self.coefficients[1] * xi + self.coefficients[2]


class LogarithmicApproximator(Approximator):
    size = 2

    def prepare(self, xs: Row) -> Row:
        minimal: Decimal = min(xs) - 1
        return super().prepare(Row([xi - minimal for xi in xs]) if minimal < 0 else xs)

    def derivatives(self, xi: Decimal) -> Row:
        return Row([xi.ln(), Decimal(1)])

    def predict_one(self, xi: Decimal) -> Decimal:
        return self.coefficients[0] * xi.ln() + self.coefficients[1]


class TrigonometricApproximator(Approximator):
    size = 2

    def derivatives(self, xi: Decimal) -> Row:
        return Row([Decimal.from_float(sin(xi)), Decimal(1)])

    def predict_one(self, xi: Decimal) -> Decimal:
        return self.coefficients[0] * Decimal.from_float(sin(xi)) + self.coefficients[1]
