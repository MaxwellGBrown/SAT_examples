"""Simple example of working w/ SAT."""
from examples import sat_utils


def implies(a, b):
    """Transform A->B into ~A or B."""
    return (sat_utils.neg(a), b)


def simple_lunch():
    """Return problem regarding whether lunch was picked up or delivered."""
    return [
        # I will order pickup OR I will order delivery
        ("pickup", "delivery"),
        # I will NOT order pickup OR I will NOT order delivery
        ("~pickup", "~delivery"),
        # It is raining OR it is NOT raining
        ("raining", "~raining"),
        # I  will pickup OR it is raining
        ("pickup", "raining"),
        # I will get delivery OR it is NOT raining
        ("delivery", "~raining"),
    ]
