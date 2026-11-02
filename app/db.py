"""A small in-memory store. Swappable for a real database behind the same functions."""
from threading import Lock
from typing import Dict, List, Optional

from .models import Issue, IssueIn, IssueUpdate

_lock = Lock()
_issues: Dict[int, Issue] = {}
_next_id = 1


def reset() -> None:
    global _next_id
    with _lock:
        _issues.clear()
        _next_id = 1


def create(data: IssueIn) -> Issue:
    global _next_id
    with _lock:
        issue = Issue(id=_next_id, **data.model_dump())
        _issues[issue.id] = issue
        _next_id += 1
        return issue


def get(issue_id: int) -> Optional[Issue]:
    return _issues.get(issue_id)


def all_issues() -> List[Issue]:
    return list(_issues.values())


def update(issue_id: int, changes: IssueUpdate) -> Optional[Issue]:
    with _lock:
        issue = _issues.get(issue_id)
        if issue is None:
            return None
        updated = issue.model_copy(update=changes.model_dump(exclude_none=True))
        _issues[issue_id] = updated
        return updated


def save(issue: Issue) -> Issue:
    with _lock:
        _issues[issue.id] = issue
        return issue
