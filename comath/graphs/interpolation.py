from decimal import Decimal

from base import Row


class Interpolator:
    def interpolate_one(self, xi: Decimal) -> Decimal:
        raise NotImplementedError()

    def interpolate_row(self, xs: Row) -> Row:
        return xs.map(self.interpolate_one)


class LagrangeInterpolator(Interpolator):
    def _coefficient(self, index: int, xs: Row, ys: Row):
        index += 1
        result: Decimal = Decimal()
        for i in range(index):
            divider = Decimal(1)
            for k in range(index):
                if k != i:
                    divider *= xs[i] - xs[k]
            result += ys[i] / divider
        return result

    def __init__(self, xs: Row, ys: Row):
        self.size: int = xs.size
        self.xs: Row = xs
        self.coefficients = [self._coefficient(i, xs, ys) for i in range(self.size)]

    def interpolate_one(self, xi: Decimal) -> Decimal:
        result: Decimal = Decimal()
        multiplier = Decimal(1)
        for i in range(self.size):
            result += multiplier * self.coefficients[i]
            multiplier *= xi - self.xs[i]
        return result


class NewtonInterpolator(Interpolator):
    def _coefficients(self, xs: Row, ys: Row) -> list[Decimal]:
        dynamic: list[list[Decimal]] = [[y for y in ys]]
        result: list[Decimal] = [dynamic[-1][0]]

        for k in range(1, xs.size):
            dynamic.append([])
            for i in range(xs.size - k):
                dynamic[-1].append((dynamic[-2][i + 1] - dynamic[-2][i])
                                   / (xs[i + k] - xs[i]))
            result.append(dynamic[-1][0])

        return result

    def __init__(self, xs: Row, ys: Row):
        self.size: int = xs.size
        self.xs: Row = xs
        self.coefficients = self._coefficients(xs, ys)

    def interpolate_one(self, xi: Decimal) -> Decimal:
        result: Decimal = Decimal()
        multiplier = Decimal(1)
        for i in range(self.size):
            result += multiplier * self.coefficients[i]
            multiplier *= xi - self.xs[i]
        return result
