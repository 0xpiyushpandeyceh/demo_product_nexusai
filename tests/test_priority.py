from datetime import datetime, timedelta, timezone

from app.models import Category, Issue, Status
from app.services.priority import score

NOW = datetime(2026, 11, 3, tzinfo=timezone.utc)


def make(category=Category.pothole, days_old=0, reports=1, status=Status.open):
    return Issue(id=1, title="Test issue", category=category, latitude=25.6, longitude=85.1,
                 created_at=NOW - timedelta(days=days_old), reports=reports, status=status)


def test_new_issue_scores_its_category_weight():
    assert score(make(Category.water), NOW) == 40


def test_age_adds_points_up_to_a_cap():
    assert score(make(days_old=5), NOW) == 45
    assert score(make(days_old=100), NOW) == 65


def test_more_reports_raise_priority():
    assert score(make(reports=3), NOW) == 45


def test_resolved_issue_has_no_priority():
    assert score(make(status=Status.resolved), NOW) == 0


def test_score_never_exceeds_100():
    assert score(make(Category.water, days_old=100, reports=50), NOW) == 100
