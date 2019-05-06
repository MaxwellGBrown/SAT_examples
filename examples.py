"""Experimentation to the pycosat SAT Solver w/ Hettinger's utils."""
import sys

import sat_utils


# Conjunctive Normal Form: A bunch of OR operations connected by AND operations
# Disjunctive Normal Form: A bunch of AND operations connected by OR operations

def implies(a, b):
    """Transform A->B into ~A or B."""
    return (sat_utils.neg(a), b)


def simple_lunch():
    """Return example of whether I ordered or purchased a lunch."""
    return [
        # I either didn't bring a lunch or didn't purchase a lunch
        implies("Brought Lunch", "~Purchased Lunch"),
        # I either brought a lunch or purchased a lunch
        implies("~Brought Lunch", "Purchased Lunch"),
        # I did not bring a lunch
        ("~Brought Lunch",),
    ]


def _readable_cnf(condition):
    # TODO Inspect condition items and determine better verbage?
    condition = [c.replace("~", "NOT ") for c in condition]
    # TODO Recursive statements?
    return " OR ".join(condition)


if __name__ == "__main__":
    try:
        _filename, puzzle_name, *_etc = sys.argv
        puzzle = locals()[puzzle_name]
    except ValueError:
        puzzle = simple_lunch
    except KeyError:
        print(f"Puzzle by name of {puzzle_name!r} does not exist.")
        exit()

    statement = puzzle()

    print("Statement\n--------")
    cnf_statement_lines = ["    AND"] * ((len(statement) * 2) - 1)
    cnf_statement_lines[0::2] = [_readable_cnf(c) for c in statement]
    for line in cnf_statement_lines:
        print(line)

    all_solutions = sat_utils.solve_all(statement)
    print('\nSolutions\n--------')
    for solution in all_solutions:
        print(_readable_cnf(solution))
