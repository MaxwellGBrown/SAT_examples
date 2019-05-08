"""Experimentation to the pycosat SAT Solver w/ Hettinger's utils."""
# import itertools

from examples import sat_utils


# Conjunctive Normal Form: A bunch of OR operations connected by AND operations
# Disjunctive Normal Form: A bunch of AND operations connected by OR operations


def comets():
    """Return a 4x4 logic square of comet discoveries."""
    # TODO Create a statement builder class
    # TODO Use a set for statement instead of += (to help avoid duplicate clauses?) # noqa
    #      In that same vein is there a way to eliminate other duplicate
    #      overriding logics?
    # TODO Abstract the ideas of comets/years/astrologers?
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
    # TODO Why does this clause take so long to run?
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
