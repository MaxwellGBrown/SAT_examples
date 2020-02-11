"""Tests for sat_examples/examples/puzzles/aerophobes.py"""
import pytest

from examples.puzzles import aerophobes
from examples import sat_utils


def test_clue_1():
    """Assert Brandi doesn't leave in March."""
    clues = (aerophobes.clue_1,)
    statement = aerophobes.aerophobes(*clues, states=False, charms=False)

    all_solutions = sat_utils.solve_all(statement)
    assert len(all_solutions) > 0

    for solution in all_solutions:
        assert aerophobes._flew_in("Brandi", "March") not in solution


def test_clue_2():
    """Assert Lee doesn't have the shamrock."""
    clues = (aerophobes.clue_2,)
    statement = aerophobes.aerophobes(*clues, states=False, months=False)

    all_solutions = sat_utils.solve_all(statement)
    assert len(all_solutions) > 0

    for solution in all_solutions:
        assert aerophobes._flew_with("Lee", "shamrock") not in solution


def test_clue_3():
    """Assert Wyoming traveler leaves 2 months before Peggy."""
    clues = (aerophobes.clue_3,)
    statement = aerophobes.aerophobes(*clues, charms=False)

    all_solutions = sat_utils.solve_all(statement)
    assert len(all_solutions) > 0

    for solution in all_solutions:
        peggy_month, wyoming_traveler = None, None
        for statement in solution:
            if statement.startswith("Peggy traveled in "):
                *_, peggy_month = statement.split("Peggy traveled in ")
            elif statement.endswith(" traveled to Wyoming"):
                wyoming_traveler, *_ = statement.split(" traveled to Wyoming")

        wyoming_month = None
        for statement in solution:
            if statement.startswith(f"{wyoming_traveler} traveled in "):
                *_, wyoming_month = statement.split(f"{wyoming_traveler} traveled in ")  # noqa

        wyoming_month_index = aerophobes.MONTHS.index(wyoming_month)
        peggy_month_index = aerophobes.MONTHS.index(peggy_month)

        assert peggy_month_index - 2 == wyoming_month_index


def test_clue_4():
    """Assert Peggy brings the horseshoe."""
    clues = (aerophobes.clue_4,)
    statement = aerophobes.aerophobes(*clues, charms=False)

    all_solutions = sat_utils.solve_all(statement)
    assert len(all_solutions) > 0

    for solution in all_solutions:
        assert aerophobes._flew_with("Peggy", "horseshoe") in solution


def test_clue_5():
    """Assert Lee leaves 1 month after Peggy."""
    clues = (aerophobes.clue_5,)
    statement = aerophobes.aerophobes(*clues, charms=False, states=False)

    all_solutions = sat_utils.solve_all(statement)
    assert len(all_solutions) > 0

    for solution in all_solutions:
        lee_month, peggy_month = None, None
        for statement in solution:
            if statement.startswith("Lee traveled in "):
                *_, lee_month = statement.split("Lee traveled in ")
            elif statement.startswith("Peggy traveled in "):
                *_, peggy_month = statement.split("Peggy traveled in ")

        print(f"Peggy {peggy_month}, Lee {lee_month}")

        peggy_month_index = aerophobes.MONTHS.index(peggy_month)
        lee_month_index = aerophobes.MONTHS.index(lee_month)

        assert peggy_month_index + 1 == lee_month_index


def test_clue_6():
    """Assert the January traveler does not have the wishbone."""
    clues = (aerophobes.clue_6,)
    statement = aerophobes.aerophobes(*clues, states=False)

    all_solutions = sat_utils.solve_all(statement)
    assert len(all_solutions) > 0

    for solution in all_solutions:
        for s in sorted(solution):
            print(s)
        print()
        january_flier = None
        for statement in solution:
            if statement.endswith(" traveled in January"):
                january_flier, *_ = statement.split(" traveled in January")
                break
        assert aerophobes._flew_with(january_flier, "wishbone") not in solution


def test_clue_7():
    """Assert the shamrock traveler leaves after Rudy."""
    clues = (aerophobes.clue_7,)
    statement = aerophobes.aerophobes(*clues, states=False)

    all_solutions = sat_utils.solve_all(statement)
    assert len(all_solutions) > 0

    for solution in all_solutions:
        rudy_month, shamrock_traveler = None, None
        for statement in solution:
            if statement.startswith("Rudy traveled in "):
                *_, rudy_month = statement.split("Rudy traveled in ")
            elif statement.endswith("'s lucky charm is a shamrock"):
                shamrock_traveler, *_ = statement.split("'s lucky charm is a shamrock")  # noqa

        # NOTE Do we want the clue to make this assumption?
        if rudy_month == "May":
            continue

        shamrock_month = None
        for statement in solution:
            if statement.startswith(f"{shamrock_traveler} traveled in "):
                *_, shamrock_month = statement.split(f"{shamrock_traveler} traveled in ")  # noqa
                break

        shamrock_month_index = aerophobes.MONTHS.index(shamrock_month)
        rudy_month_index = aerophobes.MONTHS.index(rudy_month)

        assert shamrock_month_index > rudy_month_index


def test_clue_8():
    """Assert wishbone and lucky hat are not in May."""
    statement = aerophobes.aerophobes(aerophobes.clue_8, states=False)

    all_solutions = sat_utils.solve_all(statement)
    assert len(all_solutions) > 0

    for solution in all_solutions:
        may_traveler = None
        for statement in solution:
            if statement.endswith(" traveled in May"):
                may_traveler, *_ = statement.split(" traveled in May")
                break
        assert f"{may_traveler}'s lucky charm is a wishbone" not in solution
        assert f"{may_traveler}'s lucky charm is a lucky hat" not in solution


def test_clue_9():
    """Assert Lee is either leaving in January or going to Arkansas."""
    statement = aerophobes.aerophobes(aerophobes.clue_9, charms=False)

    all_solutions = sat_utils.solve_all(statement)
    assert len(all_solutions) > 0

    for solution in all_solutions:
        lee_in_arkansas = "Lee traveled to Arkansas" in solution
        lee_on_january = "Lee traveled in January" in solution
        assert lee_in_arkansas or lee_on_january
        assert not (lee_in_arkansas and lee_on_january)


def test_clue_10():
    """Assert the flier going to Utah leaves a month before Rudy."""
    clues = (aerophobes.clue_10,)
    statement = aerophobes.aerophobes(*clues, charms=False)

    all_solutions = sat_utils.solve_all(statement)
    assert len(all_solutions) > 0

    for solution in all_solutions:
        rudy_month, utah_traveler = None, None
        for statement in solution:
            if statement.startswith("Rudy traveled in "):
                *_, rudy_month = statement.split("Rudy traveled in ")
            elif statement.endswith(" traveled to Utah"):
                utah_traveler, *_ = statement.split(" traveled to Utah")

        utah_month = None
        for statement in solution:
            if statement.startswith(f"{utah_traveler} traveled in "):
                *_, utah_month = statement.split(f"{utah_traveler} traveled in ")  # noqa

        utah_month_index = aerophobes.MONTHS.index(utah_month)
        rudy_month_index = aerophobes.MONTHS.index(rudy_month)

        assert rudy_month_index - 1 == utah_month_index


# TODO Takes too long to execute on the full problem alone. Simplify the problem?  # noqa
@pytest.mark.skip
def test_clue_11():
    """Assert the Hawaii, February, and horseshoe are different people."""
    statement = aerophobes.aerophobes(aerophobes.clue_11)

    all_solutions = sat_utils.solve_all(statement)
    assert len(all_solutions) > 0

    for solution in all_solutions:
        for name in aerophobes.FLIERS:
            going_to_hawaii = aerophobes._flew_to(name, "Hawaii") in solution
            with_horseshoe = aerophobes._flew_with(name, "horseshoe") in solution  # noqa
            in_february = aerophobes._flew_in(name, "February") in solution
            assert [going_to_hawaii, with_horseshoe, in_february].count(True) < 2  # noqa


def test_aerophobes():
    """Assert the puzzle is correct."""
    statement = aerophobes.aerophobes()
    solution, *overflow = sat_utils.solve_all(statement)

    assert not overflow
    assert sorted(solution) == [
        "Brandi traveled in January",
        "Brandi traveled to Utah",
        "Brandi's lucky charm is a lucky hat",
        "Gwen traveled in March",
        "Gwen traveled to Hawaii",
        "Gwen's lucky charm is a shamrock",
        "Lee traveled in May",
        "Lee traveled to Arkansas",
        "Lee's lucky charm is a coin",
        "Peggy traveled in April",
        "Peggy traveled to Delaware",
        "Peggy's lucky charm is a horseshoe",
        "Rudy traveled in February",
        "Rudy traveled to Wyoming",
        "Rudy's lucky charm is a wishbone",
    ]
