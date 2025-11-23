from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional

def utcnow():
    return datetime.now(timezone.utc)


class BaseTableModel(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
