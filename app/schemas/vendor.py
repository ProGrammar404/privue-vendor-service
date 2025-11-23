from typing import Optional
from sqlmodel import SQLModel, Field
from app.models.vendor import VendorCategory

class VendorCreate(SQLModel):
    name: str = Field(..., min_length=1)
    category: VendorCategory

class VendorRead(SQLModel):
    id: int
    name: str
    category: VendorCategory
    latest_score: Optional[float]
