from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional

class MetricCreate(SQLModel):
    on_time_delivery_rate: float = Field(ge=0, le=100)
    complaint_count: int = Field(ge=0)
    missing_documents: bool
    compliance_score: float = Field(ge=0, le=100)
    timestamp: Optional[datetime] = None
