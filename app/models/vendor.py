from typing import Optional, List
from sqlmodel import Field, Relationship
from enum import Enum

from app.models.base import BaseTableModel

class VendorCategory(str, Enum):
    supplier = "supplier"
    distributor = "distributor"
    dealer = "dealer"

class Vendor(BaseTableModel, table=True):
    name: str
    category: VendorCategory
    latest_score: Optional[float] = Field(default=None)

    metrics: List["VendorMetric"] = Relationship(back_populates="vendor")
    scores: List["VendorScore"] = Relationship(back_populates="vendor")


from app.models.metric import VendorMetric
from app.models.score import VendorScore
