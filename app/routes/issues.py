"""HTTP routes for issues."""
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from .. import db
from ..models import Category, Issue, IssueIn, IssueUpdate, Status

router = APIRouter(prefix="/issues", tags=["issues"])


@router.post("", response_model=Issue, status_code=status.HTTP_201_CREATED)
def report_issue(data: IssueIn) -> Issue:
    return db.create(data)


@router.get("", response_model=List[Issue])
def list_issues(category: Optional[Category] = None, status_: Optional[Status] = None, ward: Optional[str] = None) -> List[Issue]:
    items = db.all_issues()
    if category:
        items = [i for i in items if i.category == category]
    if status_:
        items = [i for i in items if i.status == status_]
    if ward:
        items = [i for i in items if (i.ward or "").lower() == ward.lower()]
    return sorted(items, key=lambda i: i.priority, reverse=True)


@router.get("/{issue_id}", response_model=Issue)
def get_issue(issue_id: int) -> Issue:
    issue = db.get(issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.patch("/{issue_id}", response_model=Issue)
def update_issue(issue_id: int, changes: IssueUpdate) -> Issue:
    issue = db.update(issue_id, changes)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue
