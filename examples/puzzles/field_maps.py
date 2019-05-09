"""Lets see if we can use CNF to perform field maps."""
import logging
import sys

import fuzzywuzzy.process

from examples import sat_utils


NULL_FIELD = {
    "label": "NOTHING",
}


log = logging.getLogger('field_maps')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


def _maps_to(incoming_field, outgoing_field):
    return f"{incoming_field} -> {outgoing_field}"


SOURCE_FIELDS = [
    {"label": "SKU"},
    {"label": "Product Name"},
    {"label": "Vendor Name"},
    {"label": "AAAAAAAAAAA"},  # Should never map to anything
]


TARGET_FIELDS = [
    {"label": "sku"},
    {"label": "name"},
    {"label": "vendor"},
    {"label": "ZZZZZZZZZZZ"},  # Nothing should have anything mapped to
]


def solve_maps(source_fields=SOURCE_FIELDS, target_fields=TARGET_FIELDS):
    """Attempt to map incoming fields to outgoing fields."""
    statement = list()

    target_labels = [field["label"] for field in target_fields]
    source_labels = [field["label"] for field in source_fields]

    # Determine what source_fields can map to which target_fields
    for target_label in target_labels:
        statement += sat_utils.one_of(
            _maps_to(source_label, target_label)
            for source_label in [*source_labels, NULL_FIELD["label"]]
        )

    # Determine what target_fields a source_field can map to
    for source_label in source_labels:
        exclusive = sat_utils.one_of(
            _maps_to(source_label, target_label)
            for target_label in [*target_labels, NULL_FIELD["label"]]
        )
        statement += exclusive

    # TODO Perhaps writing a large DNF of possibilities for a single field for
    #      all evaluations is the way to go, instead of each of them at the top
    for source_label in source_labels:
        # Fuzzy match fields by label name
        scores = fuzzywuzzy.process.extract(source_label, target_labels)
        log.debug("Scores for %r: %r", source_label, scores)
        if any(score > 70 for _, score in scores):
            fuzzy_condition = sat_utils.from_dnf([
                (_maps_to(source_label, target),)
                for target, score in scores if score > 70
            ])
            statement += fuzzy_condition

    return statement
