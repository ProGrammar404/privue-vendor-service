from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship

from app.models.base import BaseTableModel

class VendorMetric(BaseTableModel, table=True):
    vendor_id: int = Field(foreign_key="vendor.id")

    on_time_delivery_rate: float
    complaint_count: int
    missing_documents: bool
    compliance_score: float

    timestamp: datetime = Field(default_factory=datetime.utcnow)

    vendor: Optional["Vendor"] = Relationship(back_populates="metrics")


from app.models.vendor import Vendor
