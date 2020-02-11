"""Example of a 3x3 logic grid with 5 columns."""
from contextlib import contextmanager
import datetime

from examples import sat_utils


FLIERS = ("Brandi", "Gwen", "Lee", "Peggy", "Rudy")
CHARMS = ("coin", "horseshoe", "lucky hat", "shamrock", "wishbone")
STATES = ("Arkansas", "Delaware", "Hawaii", "Utah", "Wyoming")
MONTHS = ("January", "February", "March", "April", "May")


def _flew_to(name, state):
    return f"{name} traveled to {state}"


def _flew_in(name, month):
    return f"{name} traveled in {month}"


def _flew_with(name, charm):
    return f"{name}'s lucky charm is a {charm}"


@contextmanager
def timer(clue):
    """Print out timing info about the clue runtime."""
    start_time = datetime.datetime.now()
    try:
        yield clue
    finally:
        print(f"{clue} Run time: {datetime.datetime.now() - start_time}")


def clue_1(statement):
    """Brandi won't leave in March."""
    statement += [
        (
            sat_utils.neg(_flew_in("Brandi", "March")),
        )
    ]


def clue_2(statement):
    """Lee won't bring a shamrock."""
    statement += [
        (
            sat_utils.neg(_flew_with("Lee", "shamrock")),
        )
    ]


def clue_3(statement):
    """The aerophobe going to Wyoming will leave 2 months before Peggy."""
    for index in range(0, len(MONTHS)):
        peggy_month = MONTHS[index]
        if (two_months_before_index := index - 2) < 0:
            statement += [(sat_utils.neg(_flew_in("Peggy", peggy_month)),)]
            continue

        month = MONTHS[two_months_before_index]
        for name in (f for f in FLIERS if f != "Peggy"):
            statement += [
                (
                    _flew_to(name, "Wyoming"),
                    sat_utils.neg(_flew_in(name, month)),
                    sat_utils.neg(_flew_in("Peggy", peggy_month)),
                ),
                (
                    sat_utils.neg(_flew_to(name, "Wyoming")),
                    _flew_in(name, month),
                    sat_utils.neg(_flew_in("Peggy", peggy_month)),
                ),
                (
                    sat_utils.neg(_flew_to(name, "Wyoming")),
                    sat_utils.neg(_flew_in(name, month)),
                    _flew_in("Peggy", peggy_month),
                ),
            ]


def clue_4(statement):
    """Peggy will bring their horseshoe."""
    statement += [(_flew_with("Peggy", "horseshoe"),)]


def clue_5(statement):
    """Lee will leave 1 month after Peggy."""
    for index in range(len(MONTHS) - 1, -1, -1):
        month = MONTHS[index]
        if (month_before_idx := index - 1) < 0:
            statement += [(sat_utils.neg(_flew_in("Lee", month)),)]
            continue

        month_before = MONTHS[month_before_idx]
        statement += [
            (
                _flew_in("Peggy", month_before),
                sat_utils.neg(_flew_in("Lee", month)),
            ),
            (
                sat_utils.neg(_flew_in("Peggy", month_before)),
                _flew_in("Lee", month),
            ),
        ]


def clue_6(statement):
    """The aerophobe laving in January won't bring a wishbone."""
    for name in FLIERS:
        statement += [
            (
                sat_utils.neg(_flew_in(name, "January")),
                sat_utils.neg(_flew_with(name, "wishbone")),
            ),
        ]


def clue_7(statement):
    """The flier with the shamrock will leave sometime after Rudy."""
    for index in range(0, len(MONTHS)):
        rudy_months, shamrock_month = MONTHS[:index], MONTHS[index]
        for name in FLIERS:
            if not rudy_months:
                statement += [
                    (
                        sat_utils.neg(_flew_in(name, shamrock_month)),
                        sat_utils.neg(_flew_with(name, "shamrock")),
                    )
                ]
                continue
            statement += [
                (
                    # Somebody both traveling this month with shamrock...
                    sat_utils.neg(_flew_with(name, "shamrock")),
                    sat_utils.neg(_flew_in(name, shamrock_month)),
                    # ...then Rudy has to be traveling one of these months
                    *(_flew_in("Rudy", m) for m in rudy_months),  # noqa
                ),
            ]


def clue_8(statement):
    """Neither the aerophobe with the wishbone nor the one with the
       lucky hat is leaving in May.
    """
    for name in FLIERS:
        statement += [
            (
                sat_utils.neg(_flew_in(name, "May")),
                sat_utils.neg(_flew_with(name, "wishbone")),
            ),
            (
                sat_utils.neg(_flew_in(name, "May")),
                sat_utils.neg(_flew_with(name, "lucky hat")),
            ),
        ]


def clue_9(statement):
    """Lee is either the flier going to Arkansas or the flier leaving in January."""
    statement += [
        (
            _flew_to("Lee", "Arkansas"),
            _flew_in("Lee", "January"),
        ),
        (
            sat_utils.neg(_flew_to("Lee", "Arkansas")),
            sat_utils.neg(_flew_in("Lee", "January")),
        ),
    ]


def clue_10(statement):
    """The flier going to Utah will leave 1 month before Rudy."""
    for index in range(len(MONTHS) - 1, -1, -1):
        month = MONTHS[index]
        if (month_before_idx := index - 1) < 0:
            statement += [(sat_utils.neg(_flew_in("Rudy", month)),)]
            continue

        month_before = MONTHS[month_before_idx]
        for name in (f for f in FLIERS if f != "Rudy"):
            statement += [
                (
                    _flew_to(name, "Utah"),
                    sat_utils.neg(_flew_in(name, month_before)),
                    sat_utils.neg(_flew_in("Rudy", month)),
                ),
                (
                    sat_utils.neg(_flew_to(name, "Utah")),
                    _flew_in(name, month_before),
                    sat_utils.neg(_flew_in("Rudy", month)),
                ),
                (
                    sat_utils.neg(_flew_to(name, "Utah")),
                    sat_utils.neg(_flew_in(name, month_before)),
                    _flew_in("Rudy", month),
                ),
            ]


def clue_11(statement):
    """The person going to Hawaii, the one leaving in February, and the one
       with the lucky horseshoe are three different people."""
    for name in FLIERS:
        statement += [
            (
                _flew_with(name, "horseshoe"),
                sat_utils.neg(_flew_to(name, "Hawaii")),
                sat_utils.neg(_flew_in(name, "February")),
            ),
            (
                sat_utils.neg(_flew_with(name, "horseshoe")),
                _flew_to(name, "Hawaii"),
                sat_utils.neg(_flew_in(name, "February")),
            ),
            (
                sat_utils.neg(_flew_with(name, "horseshoe")),
                sat_utils.neg(_flew_to(name, "Hawaii")),
                _flew_in(name, "February"),
            ),
        ]


def aerophobes(*clues, states=True, charms=True, months=True):
    """Return a 5x5 logic square of aerophobes travel arrangements."""
    if not clues:
        clues = (
            clue_1,
            clue_2,
            clue_3,
            clue_4,
            clue_5,
            clue_6,
            clue_7,
            clue_8,
            clue_9,
            clue_10,
            clue_11,
        )

    statement = list()

    if states:
        print("States!")
        # Each person is flying to one of the destinations
        for name in FLIERS:
            statement += sat_utils.one_of(_flew_to(name, state) for state in STATES)  # noqa
        # Each destination is visited by only one person
        for state in STATES:
            statement += sat_utils.one_of(_flew_to(name, state) for name in FLIERS)  # noqa

    if charms:
        print("Charms!")
        # Each person flew with one of the charms
        for name in FLIERS:
            statement += sat_utils.one_of(_flew_with(name, charm) for charm in CHARMS)  # noqa
        # Only one of each lucky charm exists
        for charm in CHARMS:
            statement += sat_utils.one_of(_flew_with(name, charm) for name in FLIERS)  # noqa

    if months:
        print("Months!")
        # Each person flew during one of the months
        for name in FLIERS:
            statement += sat_utils.one_of(_flew_in(name, month) for month in MONTHS)  # noqa
        # Each traveler flew in a different month
        for month in MONTHS:
            statement += sat_utils.one_of(_flew_in(name, month) for name in FLIERS)  # noqa

    for clue in clues:
        with timer(clue) as clue:
            clue(statement)

    return statement
