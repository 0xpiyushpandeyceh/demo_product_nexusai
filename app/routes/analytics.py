"""Summary numbers for a ward office dashboard."""
from collections import Counter

from fastapi import APIRouter

from .. import db
from ..models import Status

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary")
def summary() -> dict:
    items = db.all_issues()
    open_items = [i for i in items if i.status != Status.resolved]
    return {
        "total": len(items),
        "open": len(open_items),
        "resolved": len(items) - len(open_items),
        "by_category": dict(Counter(i.category.value for i in items)),
        "top_priority": [i.id for i in sorted(open_items, key=lambda i: i.priority, reverse=True)[:5]],
    }
