"""Spot a report of an issue that is already open at (almost) the same place."""
from math import asin, cos, radians, sin, sqrt
from typing import Iterable, Optional

from ..models import Issue, IssueIn, Status

SAME_PLACE_METRES = 50


def distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in metres (haversine)."""
    r = 6_371_000
    p1, p2 = radians(lat1), radians(lat2)
    dp, dl = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dp / 2) ** 2 + cos(p1) * cos(p2) * sin(dl / 2) ** 2
    return 2 * r * asin(sqrt(a))


def find_duplicate(new: IssueIn, existing: Iterable[Issue]) -> Optional[Issue]:
    for issue in existing:
        if issue.status == Status.resolved or issue.category != new.category:
            continue
        if distance_m(new.latitude, new.longitude, issue.latitude, issue.longitude) <= SAME_PLACE_METRES:
            return issue
    return None
