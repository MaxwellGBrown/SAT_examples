"""Experimentation to the pycosat SAT Solver w/ Hettinger's utils."""
import datetime
import sys

from examples import sat_utils
from examples import _readable_cnf
from examples.puzzles import simple_lunch
from examples.puzzles import comets


puzzles = {
    "simple_lunch": simple_lunch.simple_lunch,
    "comets": comets.comets,
}


if __name__ == "__main__":
    try:
        _filename, puzzle_name, *_etc = sys.argv
        puzzle = puzzles[puzzle_name]
    except ValueError:
        puzzle = puzzles["simple_lunch"]
    except KeyError:
        print(f"Puzzle by name of {puzzle_name!r} does not exist.")
        exit()

    start_compose_statement = datetime.datetime.now()
    statement = puzzle()
    end_compose_statement = datetime.datetime.now()

    # print("Statement\n--------")
    # cnf_statement_lines = ["    AND"] * ((len(statement) * 2) - 1)
    # cnf_statement_lines[0::2] = [_readable_cnf(c) for c in statement]
    # for line in cnf_statement_lines:
    #     print(line)

    print("\nCalculating solutions...\n")

    start_solve_all = datetime.datetime.now()
    all_solutions = sat_utils.solve_all(statement)
    end_solve_all = datetime.datetime.now()
    print('\nSolutions\n--------')
    for num, solution in enumerate(all_solutions, start=1):
        print(f"Solution #{num}")
        print(_readable_cnf(solution, separator="\n"))
        print("\n\n")

    print(f"Statement Composition: {end_compose_statement - start_compose_statement}")  # noqa
    print(f"Solve Time: {end_solve_all - start_solve_all}")
    print(f"Total Runtime: {end_solve_all - start_compose_statement}")
