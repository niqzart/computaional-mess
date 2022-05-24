from decimal import Decimal
from typing import Protocol, Type

from base import NUMBER, number_to_decimal, Row


class EquationProtocol(Protocol):
    def __call__(self, x: Decimal, y: Decimal) -> Decimal:
        pass


class ODESolver:
    def __init__(self, step_size: Decimal, point_count: int):
        self.step_size = step_size
        self.point_count = point_count

    def _solve(self, equation: EquationProtocol, start_x: Decimal, start_y: Decimal) -> list[tuple[Decimal, Decimal]]:
        raise NotImplementedError()

    def solve(self, equation: EquationProtocol, start_x: NUMBER, start_y: NUMBER) -> list[tuple[Decimal, Decimal]]:
        return self._solve(equation, *map(number_to_decimal, (start_x, start_y)))

    def solve_as_rows(self, equation: EquationProtocol, start_x: NUMBER, start_y: NUMBER) -> tuple[Row, Row]:
        result = self.solve(equation, start_x, start_y)
        return Row([r[0] for r in result]), Row([r[1] for r in result])


class SingleStepODES(ODESolver):
    def _delta_y(self, equation: EquationProtocol, x_n: Decimal, y_n: Decimal) -> Decimal:
        raise NotImplementedError()

    def _one_step(self, equation: EquationProtocol, x_n: Decimal, y_n: Decimal) -> tuple[Decimal, Decimal]:
        return x_n + self.step_size, y_n + self.step_size * self._delta_y(equation, x_n, y_n)

    def _solve(self, equation: EquationProtocol, start_x: Decimal, start_y: Decimal) -> list[tuple[Decimal, Decimal]]:
        r = start_x, start_y
        return [r] + [r := self._one_step(equation, *r) for _ in range(self.point_count)]


class EulerODES(SingleStepODES):
    def _delta_y(self, equation: EquationProtocol, x_n: Decimal, y_n: Decimal) -> Decimal:
        return equation(x_n, y_n)


class EulerPlusODES(SingleStepODES):
    def _delta_y(self, equation: EquationProtocol, x_n: Decimal, y_n: Decimal) -> Decimal:
        t: Decimal = self.step_size / 2
        return equation(x_n + t, y_n + t * equation(x_n, y_n))


class RungeKuttaODES(SingleStepODES):
    def _delta_y(self, equation: EquationProtocol, x_n: Decimal, y_n: Decimal) -> Decimal:
        t: Decimal = self.step_size / 2
        k1: Decimal = equation(x_n, y_n)
        k2: Decimal = equation(x_n + t, y_n + t * k1)
        k3: Decimal = equation(x_n + t, y_n + t * k2)
        k4: Decimal = equation(x_n + self.step_size, y_n + self.step_size * k3)
        return (k1 + 2 * k2 + 2 * k3 + k4) / 6


class MultiStepODES(ODESolver):
    def __init__(self, starter_type: Type[SingleStepODES], step_size: Decimal, point_count: int):
        super().__init__(step_size, point_count - 4)
        self.starter: SingleStepODES = starter_type(step_size, 4)

    def _delta_y(self, y_3: Decimal, y_2: Decimal, y_1: Decimal, y_0: Decimal) -> Decimal:
        raise NotImplementedError()

    def _prev_y_index(self, current: int) -> int:
        return current + 4

    def _solve(self, equation: EquationProtocol, start_x: Decimal, start_y: Decimal) -> list[tuple[Decimal, Decimal]]:
        result = self.starter.solve(equation, start_x, start_y)
        start_x = result[-1][0]
        temp = [equation(x, y) for x, y in result]
        for i in range(self.point_count + 1):
            start_y = result[self._prev_y_index(i)][1] + self._delta_y(*(temp[(i + j) % 4] for j in range(4)))
            result.append((start_x, start_y))
            temp[i % 4] = equation(start_x, start_y)
            start_x += self.step_size
        result.pop(4)
        return result


class MilneODES(MultiStepODES):
    def _prev_y_index(self, current: int) -> int:
        return current + 1

    def _delta_y(self, y_3: Decimal, y_2: Decimal, y_1: Decimal, y_0: Decimal) -> Decimal:
        result: Decimal = 2 * y_0 - y_1 + 2 * y_2
        return Decimal(4) * self.step_size * result / Decimal(3)


class AdamsODES(MultiStepODES):
    def _delta_y(self, y_3: Decimal, y_2: Decimal, y_1: Decimal, y_0: Decimal) -> Decimal:
        result: Decimal = 55 * y_0 - 59 * y_1 + 37 * y_2 - 9 * y_3
        return self.step_size * result / Decimal(24)
