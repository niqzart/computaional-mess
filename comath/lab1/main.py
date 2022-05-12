from enum import Enum
from time import time_ns

from base import input_menu, Row, input_filename, input_int_range, input_bool
from lab1.data import EquationSystem

TIME_UNIT = "ms"


class InputType(Enum):
    KEYBOARD = "Enter a matrix from keyboard"
    FILE = "Read a matrix from file"
    RANDOM = "Generate a random matrix"
    EXIT = "Quit"


if __name__ == "__main__":
    while True:
        try:
            es: EquationSystem
            solution: Row
            triangle: EquationSystem
            generated: Row | None = None
            elapsed_time: int

            match input_menu(InputType, "Enter the preferred input method: "):
                case InputType.KEYBOARD:
                    es = EquationSystem.from_input()
                    elapsed_time = time_ns()
                    solution, triangle = es.wild_solve()
                    elapsed_time = time_ns() - elapsed_time
                case InputType.FILE:
                    filename = input_filename("Enter the filename: ")
                    with open(filename) as f:
                        es = EquationSystem.from_file(f)
                    elapsed_time = time_ns()
                    solution, triangle = es.wild_solve()
                    elapsed_time = time_ns() - elapsed_time
                case InputType.RANDOM:
                    ints_only = input_bool("Do you want to use integers only? ")
                    print("Interpreting as", "Yes" if ints_only else "No")
                    row_count = input_int_range("Enter the row count (2 to 20): ", 2, 21)
                    # noinspection PyRedeclaration
                    es, solution, triangle, generated, elapsed_time = \
                        EquationSystem.from_random(row_count, allow_floats=not ints_only)
                case InputType.EXIT:
                    break

            print("Input Matrix:")
            print(es, end="\n\n")
            print("Triangle Matrix:")
            print(triangle, end="\n\n")

            print("Solution:", solution)
            print("Residuals:", es.residuals(solution), end="\n\n")
            if generated is not None:
                print("Generated Inputs:", generated)
                print("Difference From Solution:", es.residuals(generated), end="\n\n")

            match TIME_UNIT:
                case "µs":
                    print("Time Elapsed (µs):", elapsed_time / 1000)
                case "ms":
                    print("Time Elapsed (ms):", elapsed_time / 1000000)
                case _:
                    print("Time Elapsed (ns):", elapsed_time)
            break
        except ValueError as e:
            print("ERROR:", e.args[0], end="\n\n")
