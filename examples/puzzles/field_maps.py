"""Lets see if we can use CNF to perform field maps."""
import logging
import sys

import fuzzywuzzy.process

from examples import sat_utils


log = logging.getLogger('field_maps')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


class Field:
    """Representation of a field to me mapped from/to."""

    def __init__(self, label):
        """Init Field."""
        self.label = label

    def __repr__(self):
        """Return repr of Field instance."""
        return f"<Field(label={self.label!r})>"

    def __str__(self):
        """Return str value of Field instance."""
        return self.label


class Mapping:
    """Represents a mapping between two fields."""

    def __init__(self, source_field, target_field):
        """Init Mapping with source_field -> target_field."""
        self.source_field = source_field
        self.target_field = target_field

    def __repr__(self):
        """Return repr of Mapping instance."""
        return f"<Mapping(source_field={self.source_field}," \
               "{self.target_field})>"

    def __str__(self):
        """Return str representation of Mapping instance."""
        return f"{self.source_field} -> {self.target_field}"


SOURCE_FIELDS = [
    Field("SKU"),
    Field("Product Name"),
    Field("Vendor Name"),
    Field("Duplicate"),
    Field("AAAAAAAAAA"),  # Should never map to anything
]


TARGET_FIELDS = [
    Field("sku"),
    Field("name"),
    Field("vendor"),
    Field("Duplicate"),
    Field("ZZZZZZZZZZZ"),  # Nothing should have anything mapped to
]


NULL_FIELD = Field("NOTHING")


# TODO Need to teach the statement to prefer mapping to NOTHING over mapping to
#      an unmapped field.


def solve_maps(source_fields=SOURCE_FIELDS, target_fields=TARGET_FIELDS):
    """Attempt to map incoming fields to outgoing fields."""
    statement = list()

    source_possibilities = {f: {NULL_FIELD} for f in source_fields}
    target_possibilities = {f: {NULL_FIELD} for f in target_fields}

    # TODO Perhaps writing a large DNF of possibilities for a single field for
    #      all evaluations is the way to go, instead of each of them at the top
    targets_by_label = {str(field): field for field in target_fields}
    for source_field in source_fields:
        # Fuzzy match fields by label name
        scores = fuzzywuzzy.process.extract(str(source_field), targets_by_label.keys())  # noqa
        log.debug("Scores for %s: %r", source_field, scores)
        passing_scores = [score for score in scores if score[1] > 70]
        if passing_scores:
            source_possibilities[source_field].update(
                targets_by_label[label] for label, score in passing_scores
            )
            for label, _score in passing_scores:
                target_field = targets_by_label[label]
                target_possibilities[target_field].add(source_field)

            fuzzy_condition = sat_utils.from_dnf([
                (str(Mapping(source_field, targets_by_label[target_label])),)
                for target_label, score in scores if score > 70
            ])
            log.debug(fuzzy_condition)
            statement += fuzzy_condition

    # Determine what source_fields can map to which target_fields
    for target_field in target_fields:
        statement += sat_utils.one_of(
            str(Mapping(source_field, target_field))
            for source_field in target_possibilities[target_field]
        )

    # Determine what target_fields a source_field can map to
    for source_field in source_fields:
        statement += sat_utils.one_of(
            str(Mapping(source_field, target_field))
            for target_field in source_possibilities[source_field]
        )

    return statement
