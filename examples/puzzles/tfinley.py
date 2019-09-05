"""Do the thing."""


def tfinley():
    """Return the example problem from the internet.

    I swear this problem has more than once answer but they only show the one
    answer. So I'm here to check it.

    http://tfinley.net/software/pyglpk/ex_sat.html
    """
    return [
        ("~a", "~c", "~d"),
        ("b", "c", "d"),
        ("a", "~b", "d"),
        ("a", "c", "d"),
        ("~a", "b", "~c"),
    ]
