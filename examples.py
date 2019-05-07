"""Experimentation to the pycosat SAT Solver w/ Hettinger's utils."""
import datetime
import itertools
import sys

import sat_utils


# Conjunctive Normal Form: A bunch of OR operations connected by AND operations
# Disjunctive Normal Form: A bunch of AND operations connected by OR operations

def implies(a, b):
    """Transform A->B into ~A or B."""
    return (sat_utils.neg(a), b)


def grouper(n, iterable, fillvalue=None):
    """Group iterable in chunks."""
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)


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


def comets():
    """Return a 4x4 logic square of comet discoveries."""
    def _discovered_by(comet, astrologer):
        return f"{comet} was discovered by {astrologer}"

    def _discovered_in(comet, year):
        return f"{comet} was discovered in {year}"

    comets = ("Casputi", "Crecci", "Peinope", "Sporrin")
    years = ("2008", "2009", "2010", "2011")
    astrologers = ("Hal Gregory", "Jack Ingram", "Ken Jones", "Underwood")

    statement = list()

    for comet in comets:
        # Each comet was discovered in one of these years
        statement += sat_utils.one_of(_discovered_in(comet, year) for year in years)  # noqa
        # Each comet was discovered by one of these people
        statement += sat_utils.one_of(_discovered_by(comet, astrologer) for astrologer in astrologers)  # noqa

    # Each year is applied to exactly one comet
    for year in years:
        statement += sat_utils.one_of(_discovered_in(comet, year) for comet in comets)  # noqa
    # Each astrologer discovered exactly one comet
    for astrologer in astrologers:
        statement += sat_utils.one_of(_discovered_by(comet, astrologer) for comet in comets)  # noqa

    # Clues

    # The one discovered in 2009 is Casputi
    # =========================================================================
    statement += [(_discovered_in("Casputi", "2009"),)]
    # =========================================================================

    # The one Jack Ingram discovered was found in 2008
    # =========================================================================
    statement += sat_utils.from_dnf([
        (
            _discovered_by(comet, "Jack Ingram"),
            _discovered_in(comet, "2008"),
        )
        for comet in comets
    ])
    # =========================================================================

    # The comet Underwood discovered was discovered 2 years
    # after the comet Jack Ingram Discovered
    # =========================================================================
    # dnf = list()
    # for comet_1, comet_2 in itertools.permutations(comets, 2):
    #     for index in range(len(comets) - 2):
    #         dnf += [
    #             (
    #                 _discovered_by(comet_1, "Underwood"),
    #                 _discovered_in(comet_1, years[index + 2]),
    #                 _discovered_by(comet_2, "Jack Ingram"),
    #                 _discovered_in(comet_2, years[index])
    #             ),
    #         ]
    # print("Generating 'Discovered 2 years later clause...'")
    # cnf = sat_utils.from_dnf(dnf)
    # statement += cnf
    # =========================================================================

    # Peinope was discovered 1 year before the one Hal Gregory discovered
    # =========================================================================
    dnf = list()
    for comet in comets:
        for index in range(len(years) - 1, 0, -1):
            dnf += [
                (
                    _discovered_in("Peinope", years[index - 1]),
                    _discovered_in(comet, years[index]),
                    _discovered_by(comet, "Hal Gregory"),
                )
            ]
    cnf = sat_utils.from_dnf(dnf)
    statement += cnf
    # =========================================================================

    # The comet discovered in 2010 is either
    # the one Ken Jones discovered or Crecci
    # =========================================================================
    for comet in comets:
        statement += sat_utils.from_dnf([
            # TODO I'm doing too much human-logic here; the statement proper
            #      must somehow be easier to represent
            (
                # ...discovered in 2010 by Ken Jones
                _discovered_in(comet, "2010"),
                _discovered_by(comet, "Ken Jones"),
                # ...therefore it is not Crecci
                sat_utils.neg(_discovered_in("Crecci", "2010")),
                sat_utils.neg(_discovered_by("Crecci", "Ken Jones")),
            ),
            (
                # ...Crecci discovered in 2010
                _discovered_in("Crecci", "2010"),
                # ...therefor not discovered by Ken Jones
                sat_utils.neg(_discovered_by("Crecci", "Ken Jones")),
            ),
        ])
    # =========================================================================

    return statement


def _readable_cnf(condition, separator=" OR "):
    # TODO Inspect condition items and determine better verbage?
    condition = [c.replace("~", "NOT ") for c in condition]
    # TODO Recursive statements?
    return separator.join(condition)


if __name__ == "__main__":
    try:
        _filename, puzzle_name, *_etc = sys.argv
        puzzle = locals()[puzzle_name]
    except ValueError:
        puzzle = simple_lunch
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

    print(f"Statement Composition: {end_compose_statement - start_compose_statement}")
    print(f"Solve Time: {end_solve_all - start_solve_all}")
    print(f"Total Runtime: {end_solve_all - start_compose_statement}")
