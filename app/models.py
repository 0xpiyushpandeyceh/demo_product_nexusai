"""Data model for a reported civic issue."""
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Category(str, Enum):
    pothole = "pothole"
    streetlight = "streetlight"
    garbage = "garbage"
    water = "water"
    other = "other"


class Status(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"


class IssueIn(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(default="", max_length=2000)
    category: Category
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    ward: Optional[str] = None


class Issue(IssueIn):
    id: int
    status: Status = Status.open
    reports: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    priority: float = 0.0


class IssueUpdate(BaseModel):
    status: Optional[Status] = None
    description: Optional[str] = Field(default=None, max_length=2000)
