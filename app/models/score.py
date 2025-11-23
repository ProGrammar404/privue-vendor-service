from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship

from app.models.base import BaseTableModel, utcnow

class VendorScore(BaseTableModel, table=True):
    vendor_id: int = Field(foreign_key="vendor.id")
    score: float
    calculated_at: datetime = Field(default_factory=utcnow)
    
    vendor: Optional["Vendor"] = Relationship(back_populates="scores")

from app.models.vendor import Vendor
