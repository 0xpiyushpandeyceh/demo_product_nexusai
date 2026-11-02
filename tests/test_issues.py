import pytest
from fastapi.testclient import TestClient

from app import db
from app.main import app
from app.services.duplicates import distance_m

client = TestClient(app)
PATNA = {"latitude": 25.6093, "longitude": 85.1376}


@pytest.fixture(autouse=True)
def clean():
    db.reset()


def report(**extra):
    body = {"title": "Pothole near the bus stand", "category": "pothole", **PATNA, **extra}
    return client.post("/issues", json=body)


def test_report_and_fetch_an_issue():
    r = report()
    assert r.status_code == 201
    issue = r.json()
    assert issue["priority"] > 0
    assert client.get(f"/issues/{issue['id']}").json()["title"] == "Pothole near the bus stand"


def test_a_second_report_at_the_same_place_raises_the_existing_issue():
    first = report().json()
    second = report(latitude=PATNA["latitude"] + 0.0001).json()  # about 11 metres away
    assert second["id"] == first["id"]
    assert second["reports"] == 2
    assert len(client.get("/issues").json()) == 1


def test_a_report_far_away_is_a_new_issue():
    report()
    report(latitude=PATNA["latitude"] + 0.01)  # about 1.1 km away
    assert len(client.get("/issues").json()) == 2


def test_resolve_an_issue():
    issue = report().json()
    r = client.patch(f"/issues/{issue['id']}", json={"status": "resolved"})
    assert r.json()["status"] == "resolved"


def test_unknown_issue_is_404():
    assert client.get("/issues/999").status_code == 404


def test_invalid_coordinates_are_rejected():
    assert report(latitude=200).status_code == 422


def test_distance_is_roughly_right():
    assert 1000 < distance_m(25.6, 85.1, 25.61, 85.1) < 1200


def test_summary_counts():
    report()
    report(category="garbage", latitude=25.7)
    s = client.get("/analytics/summary").json()
    assert s["total"] == 2 and s["open"] == 2 and s["by_category"]["garbage"] == 1
