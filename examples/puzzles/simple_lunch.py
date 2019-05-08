"""Simple example of working w/ SAT."""
from examples import sat_utils


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
