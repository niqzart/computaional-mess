from __future__ import annotations

from decimal import Decimal, DecimalException
from random import random, seed
from time import time_ns
from typing import TextIO

from base import Matrix, Row


class EquationSystem(Matrix):
    @classmethod
    def from_input(cls) -> EquationSystem:
        i: int = 0
        rows: list[Row] = []
        row_size: int | None = None

        while True:
            line: str = input(f"Enter row #{i + 1}" + ("" if row_size is None else f" ({row_size} numbers)") + ": ")
            try:
                row = Row.from_line(line.strip())
            except ValueError as e:
                print(e.args[0])
                continue

            if row_size is None:
                row_size = row.size
            elif row_size != row.size:
                if row_size < row.size:
                    print(f"Input format error: too many numbers in the row")
                else:
                    print(f"Input format error: too few numbers in the row")
                continue

            rows.append(row)
            i += 1
            if i == row_size - 1:
                break

        return cls(rows)

    @classmethod
    def from_file(cls, file: TextIO):
        lines: list[str] = file.read().strip().replace("\n\r", "\n").split("\n")
        if lines[0].count(" ") < 2:
            lines.pop(0)
        result = cls.from_lines(lines)
        if result.size[0] != result.size[1] - 1:
            raise ValueError(f"Input format error: {result.size} is a wrong matrix size for this task")
        return result

    @classmethod
    def from_random(cls, row_count: int, allow_floats: bool = True, seed_value=None) \
            -> tuple[EquationSystem, Row, EquationSystem, Row, int]:
        if seed_value is not None:
            seed(seed_value)

        def generate(_):
            result = random() * 20 - 10
            if allow_floats:
                return Decimal(str(result)) + Decimal(str(random())) * Decimal("0.00000000001")
            return Decimal(int(result))

        generated: Row = Row.from_lambda(row_count, generate)
        A: Matrix = Matrix([Row.from_lambda(row_count, generate) for _ in range(row_count)])
        B = A * generated
        result = EquationSystem([Row([*row, B[i]]) for i, row in enumerate(A)])

        try:
            elapsed_time: int = time_ns()
            solution, triangle = result.copy().solve()
            return result, solution, triangle, generated, time_ns() - elapsed_time
        except DecimalException:
            if seed_value is not None:
                raise ValueError(f"Can't generate a valid matrix with seed: {seed}")
            return cls.from_random(row_count, allow_floats, seed_value)

    def copy(self):
        return EquationSystem([item.copy() for item in self], self.size)

    def max(self, exclude_np1: bool = True, absolute: bool = True) -> Decimal:
        key = abs if absolute else None
        return max((max(row[:-1] if exclude_np1 else row, key=key) for row in self), key=key)

    def _row_pivot(self, i, row) -> tuple[int, int, Decimal]:
        result = max(enumerate(row[:-1]), key=lambda x: abs(x[1]))
        return i, result[0], result[1]

    def pivot_element(self) -> tuple[int, int, Decimal]:
        return max((self._row_pivot(i, row)
                    for i, row in enumerate(self)), key=lambda x: abs(x[2]))

    def _solve(self, result_mapping: list[int] = None) \
            -> dict[int, tuple[Decimal, Row, list[int]]]:
        if result_mapping is None:
            result_mapping = list(range(self.size[0]))
        if len(result_mapping) == 0:
            return {}

        p, q, value = self.pivot_element()
        main_row = self[p].copy()

        for i in range(self.size[0]):
            if i == p:
                continue
            coefficient: Decimal = -(self[i][q] / value)
            self[i] += main_row * coefficient

        self.drop_row(p)
        self.drop_column(q)
        rm = result_mapping.copy()
        result_index = result_mapping.pop(q)

        result_dict = self._solve(result_mapping)
        result: Decimal = main_row[-1]
        for i, x in result_dict.items():
            result -= main_row[rm.index(i)] * x[0]
        result /= main_row[q]
        result_dict[result_index] = result, main_row, rm

        return result_dict

    def solve(self) -> tuple[Row, EquationSystem]:
        result = self._solve()

        def triangle_row_sort(args):
            i, row = args
            if i == len(triangle) - 1:
                return -1
            return row.data.count(Decimal(0))

        triangle = EquationSystem(
            [Row([*(row[rm.index(i)] if i in rm else 0
                    for i in range(len(result))), row[-1]])
             for _, row, rm in reversed(result.values())])
        triangle.transpose()
        columns = sorted(enumerate(triangle), key=triangle_row_sort, reverse=True)
        triangle = EquationSystem([column for _, column in columns])
        triangle.transpose()

        return Row([x[1] for x in sorted([
            (k, v[0]) for k, v in result.items()], key=lambda x: x[0])]), triangle

    def wild_solve(self) -> tuple[Row, EquationSystem]:
        try:
            return self.copy().solve()
        except DecimalException:
            raise ValueError("Matrix is non-convergent")

    def residuals(self, solution: Row) -> Row:
        A: Matrix = self.copy()
        B: Row = A.drop_column(-1)
        R: Row = A * solution
        return abs(B - R)
