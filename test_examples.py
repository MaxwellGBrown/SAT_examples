"""Tests for the puzzles, so I can refactor them without going crazy."""
import examples
import sat_utils


def test_comets():
    """Assert the comets problem is solved correctly."""
    statement = examples.comets()
    solutions = sat_utils.solve_all(statement)

    assert len(solutions) == 1

    readable_statement = examples._readable_cnf(solutions[0], separator="\n")
    assertions = readable_statement.split("\n")

    expected = [
        "Casputi was discovered in 2009",
        "Casputi was discovered by Hal Gregory",
        "Crecci was discovered in 2010",
        "Crecci was discovered by Underwood",
        "Peinope was discovered in 2008",
        "Peinope was discovered by Jack Ingram",
        "Sporrin was discovered in 2011",
        "Sporrin was discovered by Ken Jones",
    ]

    for assertion in expected:
        assert assertion in assertions
