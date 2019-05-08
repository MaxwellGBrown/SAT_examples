def _readable_cnf(condition, separator=" OR "):
    # TODO Inspect condition items and determine better verbage?
    condition = [c.replace("~", "NOT ") for c in condition]
    # TODO Recursive statements?
    return separator.join(condition)
