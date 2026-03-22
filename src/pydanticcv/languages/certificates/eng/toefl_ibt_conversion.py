"""ETS official TOEFL iBT score conversion tables (legacy 0-30/0-120 ↔ new 1-6 scale).

ETS introduced a new 1-6 scoring scale in January 2026.  This module contains
the official per-section lookup tables and the total-score threshold table
published by ETS, plus derived reverse tables for converting back from the
new scale to the legacy scale.

Source:
    https://www.ets.org/toefl/institutions/ibt/score-scale-update.html

Contents:
    READING_TO_NEW: Legacy Reading score (0-30) → new score (1-6).
    LISTENING_TO_NEW: Legacy Listening score (0-30) → new score (1-6).
    WRITING_TO_NEW: Legacy Writing score (0-30) → new score (1-6).
    SPEAKING_TO_NEW: Legacy Speaking score (0-30) → new score (1-6).
    READING_TO_LEGACY: New Reading score (1-6) → max legacy score (0-30).
    LISTENING_TO_LEGACY: New Listening score (1-6) → max legacy score (0-30).
    WRITING_TO_LEGACY: New Writing score (1-6) → max legacy score (0-30).
    SPEAKING_TO_LEGACY: New Speaking score (1-6) → max legacy score (0-30).
    total_legacy_to_new: Convert a legacy total score (0-120) to the new scale.
"""

__all__ = [
    "READING_TO_NEW",
    "LISTENING_TO_NEW",
    "WRITING_TO_NEW",
    "SPEAKING_TO_NEW",
    "READING_TO_LEGACY",
    "LISTENING_TO_LEGACY",
    "WRITING_TO_LEGACY",
    "SPEAKING_TO_LEGACY",
    "total_legacy_to_new",
]

# ---------------------------------------------------------------------------
# Section-level: old 0-30 → new 1-6
# Each section has its own table as the mapping differs per skill.
# ---------------------------------------------------------------------------
READING_TO_NEW: dict[int, float] = {
    30: 6.0,
    29: 6.0,
    28: 5.5,
    27: 5.5,
    26: 5.0,
    25: 5.0,
    24: 5.0,
    23: 4.5,
    22: 4.5,
    21: 4.0,
    20: 4.0,
    19: 4.0,
    18: 4.0,
    17: 3.5,
    16: 3.5,
    15: 3.5,
    14: 3.5,
    13: 3.5,
    12: 3.5,
    11: 3.0,
    10: 3.0,
    9: 3.0,
    8: 3.0,
    7: 3.0,
    6: 3.0,
    5: 2.5,
    4: 2.5,
    3: 2.0,
    2: 1.5,
    1: 1.0,
    0: 1.0,
}
LISTENING_TO_NEW: dict[int, float] = {
    30: 6.0,
    29: 6.0,
    28: 6.0,
    27: 5.5,
    26: 5.5,
    25: 5.0,
    24: 5.0,
    23: 5.0,
    22: 5.0,
    21: 4.5,
    20: 4.5,
    19: 4.0,
    18: 4.0,
    17: 4.0,
    16: 3.5,
    15: 3.5,
    14: 3.5,
    13: 3.5,
    12: 3.0,
    11: 3.0,
    10: 3.0,
    9: 3.0,
    8: 2.5,
    7: 2.5,
    6: 2.5,
    5: 2.0,
    4: 2.0,
    3: 1.5,
    2: 1.5,
    1: 1.0,
    0: 1.0,
}
WRITING_TO_NEW: dict[int, float] = {
    30: 6.0,
    29: 6.0,
    28: 5.5,
    27: 5.5,
    26: 5.0,
    25: 5.0,
    24: 5.0,
    23: 4.5,
    22: 4.5,
    21: 4.5,
    20: 4.0,
    19: 4.0,
    18: 4.0,
    17: 4.0,
    16: 3.5,
    15: 3.5,
    14: 3.0,
    13: 3.0,
    12: 2.5,
    11: 2.5,
    10: 2.0,
    9: 2.0,
    8: 2.0,
    7: 2.0,
    6: 1.5,
    5: 1.5,
    4: 1.5,
    3: 1.5,
    2: 1.0,
    1: 1.0,
    0: 1.0,
}
SPEAKING_TO_NEW: dict[int, float] = {
    30: 6.0,
    29: 6.0,
    28: 6.0,
    27: 5.5,
    26: 5.0,
    25: 5.0,
    24: 4.5,
    23: 4.5,
    22: 4.0,
    21: 4.0,
    20: 4.0,
    19: 3.5,
    18: 3.5,
    17: 3.0,
    16: 3.0,
    15: 2.5,
    14: 2.5,
    13: 2.5,
    12: 2.0,
    11: 2.0,
    10: 2.0,
    9: 1.5,
    8: 1.5,
    7: 1.5,
    6: 1.5,
    5: 1.5,
    4: 1.0,
    3: 1.0,
    2: 1.0,
    1: 1.0,
    0: 1.0,
}

# Reverse tables: new 1-6 → max legacy score that maps to it (upper-bound approximation).
# Because multiple legacy values map to the same new value the reverse is not
# unique; we use the highest possible legacy value as the upper-bound estimate.
READING_TO_LEGACY: dict[float, int] = {
    v: max(k for k, nv in READING_TO_NEW.items() if nv == v)
    for v in set(READING_TO_NEW.values())
}
LISTENING_TO_LEGACY: dict[float, int] = {
    v: max(k for k, nv in LISTENING_TO_NEW.items() if nv == v)
    for v in set(LISTENING_TO_NEW.values())
}
WRITING_TO_LEGACY: dict[float, int] = {
    v: max(k for k, nv in WRITING_TO_NEW.items() if nv == v)
    for v in set(WRITING_TO_NEW.values())
}
SPEAKING_TO_LEGACY: dict[float, int] = {
    v: max(k for k, nv in SPEAKING_TO_NEW.items() if nv == v)
    for v in set(SPEAKING_TO_NEW.values())
}

# ---------------------------------------------------------------------------
# Total score: old 0-120 → new 1-6 (lower-bound thresholds, per ETS table)
# ---------------------------------------------------------------------------
_TOTAL_THRESHOLDS: list[tuple[int, float]] = [
    (114, 6.0),
    (107, 5.5),
    (95, 5.0),
    (86, 4.5),
    (72, 4.0),
    (58, 3.5),
    (44, 3.0),
    (34, 2.5),
    (24, 2.0),
    (12, 1.5),
    (0, 1.0),
]


def total_legacy_to_new(total: int) -> float:
    """Convert a legacy TOEFL total score (0-120) to the new 1-6 scale.

    Uses the official ETS lower-bound threshold table.  The returned value
    is the new-scale equivalent for the highest threshold that ``total``
    meets or exceeds.

    Args:
        total: Legacy total score in the range 0-120.

    Returns:
        Equivalent score on the new 1-6 scale (in 0.5 steps).
    """
    for threshold, new_score in _TOTAL_THRESHOLDS:
        if total >= threshold:
            return new_score
    return 1.0  # unreachable
