from __future__ import annotations

from decimal import Decimal
from typing import Callable

from .utils import NUMBER, number_to_decimal, beautify_decimal


class Row:
    def __init__(self, data: list[NUMBER] = None, size: int = None):
        if data is None:
            self.data: list[Decimal] = []
        else:
            self.data: list[Decimal] = [number_to_decimal(number) for number in data]
        self.size: int = size or len(self.data)

    @classmethod
    def from_line(cls, number_line: str, number_separator: str = None) -> Row:
        return cls([number_to_decimal(number_str) for number_str in number_line.split(number_separator)])

    @classmethod
    def from_lambda(cls, size: int, value: Callable[[int], Decimal] = lambda i: Decimal()):
        return cls([value(i) for i in range(size)], size)

    def __getitem__(self, item: int) -> Decimal:
        return self.data[item]

    def __setitem__(self, key: int, value: NUMBER) -> None:
        if key >= self.size:
            raise IndexError()
        self.data[key] = number_to_decimal(value)

    def __len__(self) -> int:
        return self.size

    def __iter__(self):
        return iter(self.data)

    def copy(self):
        return Row([item for item in self], self.size)

    def __pos__(self):
        return self

    def __neg__(self):
        return Row([-item for item in self])

    def _check_size(self, other):
        if not isinstance(other, Row):
            raise TypeError()
        if self.size != other.size:
            raise ValueError()

    def __abs__(self) -> Row:
        return Row([abs(item) for item in self])

    def __add__(self, other: Row) -> Row:
        self._check_size(other)
        return Row([self[i] + other[i] for i in range(self.size)])

    def __sub__(self, other):
        self._check_size(other)
        return Row([self[i] - other[i] for i in range(self.size)])

    def __mul__(self, other: NUMBER):
        other = number_to_decimal(other)
        return Row([item * other for item in self])

    def __truediv__(self, other: NUMBER):
        other = number_to_decimal(other)
        if other == 0:
            raise ZeroDivisionError()

        return Row([item / other for item in self])

    def pop(self, index: int):
        self.size -= 1
        return self.data.pop(index)

    def __repr__(self):
        return f"Row[{self.size}]: {self.data}"

    def to_str(self, quantize: bool = True):
        result = ""
        for i, item in enumerate(self.data):
            if i != 0:
                result += " "
            result += beautify_decimal(item, quantize)
        return result

    def to_non_rounded_str(self):
        return self.to_str(False)

    def __str__(self):
        return self.to_str()


class Matrix:
    def __init__(self, data: list[Row] = None, size: tuple[int, int] = None):
        if data is not None and len(data) > 1:
            row_size = data[0].size
            for row in data[1:]:
                if row.size != row_size:
                    raise ValueError("Row size can't differ for a matrix")
        else:
            row_size = 0

        self.data: list[Row] = data or []
        self.size: tuple[int, int] = size or (len(self.data), row_size)
        self.column_picker: ColumnPicker = ColumnPicker(self)

    @classmethod
    def from_lines(cls, lines: list[str], number_separator: str = None) -> Matrix:
        return cls([Row.from_line(line, number_separator) for line in lines])

    @classmethod
    def from_text(cls, text: str, line_separator: str = None, number_separator: str = None) -> Matrix:
        return cls.from_lines(text.split(line_separator or "\n"), number_separator)

    @classmethod
    def from_lambda(cls, size: tuple[int, int], value: Callable[[int, int], Decimal] = lambda i, j: Decimal()):
        return cls([Row.from_lambda(size[1], lambda j: value(i, j)) for i in range(size[0])], size)

    def __getitem__(self, item: int | ellipsis) -> Row | ColumnPicker:
        if item is ...:
            return self.column_picker
        return self.data[item]

    def __setitem__(self, key: int, value: Row) -> None:
        if key >= self.size[0]:
            raise IndexError()
        self.data[key] = value

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return self.size[0]

    def copy(self):
        return Matrix([item.copy() for item in self], self.size)

    def __pos__(self):
        return self

    def __neg__(self):
        return Matrix([-item.copy() for item in self], self.size)

    def _check_size(self, other):
        if not isinstance(other, Matrix):
            raise TypeError()
        if self.size != other.size:
            raise ValueError()

    def __add__(self, other: Matrix) -> Matrix:
        self._check_size(other)
        return Matrix([self[i] + other[i] for i in range(self.size[0])])

    def __sub__(self, other: Matrix) -> Matrix:
        self._check_size(other)
        return Matrix([self[i] + other[i] for i in range(self.size[0])])

    def _mult_item(self, other: Matrix, i: int, j: int) -> Decimal:
        return sum(self[i][k] * other[k][j] for k in range(self.size[1]))

    def __mul__(self, other: Matrix | Row | NUMBER) -> Matrix | Row:
        if isinstance(other, Matrix):
            return Matrix([
                Row([self._mult_item(other, i, j) for j in range(other.size[1])])
                for i in range(self.size[0])
            ])

        if isinstance(other, Row):
            return Row([sum(self[i][k] * other[k] for k in range(self.size[1])) for i in range(self.size[0])])

        other = number_to_decimal(other)
        return Matrix([item * other for item in self])

    def __truediv__(self, other: NUMBER) -> Matrix:
        other = number_to_decimal(other)
        if other == 0:
            raise ZeroDivisionError()

        return Matrix([item / other for item in self])

    def __pow__(self, power: int, modulo=None) -> Matrix:
        if not isinstance(power, int):
            raise TypeError()
        if power == -1:
            return self.reverse_matrix()
        if power < 1:
            raise ValueError()

        result = self.copy()
        for _ in range(power - 1):
            result *= self
        return result

    def drop_row(self, index: int):
        self.size = self.size[0] - 1, self.size[1]
        return self.data.pop(index)

    def drop_column(self, index: int):
        self.size = self.size[0], self.size[1] - 1
        return Row([row.pop(index) for row in self])

    def transpose(self) -> None:
        self.data = [Row([self[j][i] for j in range(self.size[0])]) for i in range(self.size[1])]
        self.size = self.size[1], self.size[0]

    def transpose_copy(self) -> Matrix:
        result = self.copy()
        result.transpose()
        return result

    def cofactor(self, i: int, j: int) -> Decimal:
        result = self.copy()
        result.drop_row(i)
        result.drop_column(j)
        if (i + j) % 2 == 0:
            return result.determinant()
        return -result.determinant()

    def determinant(self) -> Decimal:
        if self.size[0] != self.size[1]:
            raise ValueError()

        if self.size[0] == 1:
            return self.data[0][0]

        result = Decimal()
        for i in range(self.size[0]):
            if self[0][i] != 0:
                result += self[0][i] * self.cofactor(0, i)
        return result

    def reverse_matrix(self) -> Matrix:
        pass

    def debug_str(self, separate_lines: bool = True, prefix: bool = True):
        result: str = f"Matrix[{self.size}]: {{" if prefix else "{"
        if separate_lines:
            result += "\n"
        for row in self:
            result += f" {str(row)}"
            result += "\n" if separate_lines else ","
        result += "}"
        return result

    def __repr__(self):
        return self.debug_str(False)

    def __str__(self):
        return self.debug_str(prefix=False)


class ColumnPicker:
    def __init__(self, matrix: Matrix):
        self.matrix = matrix

    def __getitem__(self, item) -> Row:
        return Row([row[item] for row in self.matrix])
