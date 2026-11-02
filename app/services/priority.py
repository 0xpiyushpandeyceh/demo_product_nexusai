"""Priority score for an issue: how urgently a ward office should act on it (0-100)."""
from datetime import datetime, timezone

from ..models import Category, Issue, Status

# How serious each kind of problem is on its own.
CATEGORY_WEIGHT = {
    Category.water: 40,
    Category.pothole: 35,
    Category.streetlight: 25,
    Category.garbage: 20,
    Category.other: 10,
}
MAX_AGE_POINTS = 30      # an issue left open gains up to 30 points over 15 days
MAX_REPORT_POINTS = 30   # each extra citizen report adds 5 points, up to 30


def score(issue: Issue, now: datetime | None = None) -> float:
    if issue.status == Status.resolved:
        return 0.0
    now = now or datetime.now(timezone.utc)
    age_days = max((now - issue.created_at).total_seconds() / 86400, 0)
    age_points = min(age_days * 2, MAX_AGE_POINTS)
    report_points = min((issue.reports - 1) * 5, MAX_REPORT_POINTS)
    return round(min(CATEGORY_WEIGHT[issue.category] + age_points + report_points, 100), 1)
