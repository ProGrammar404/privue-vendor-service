from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.vendor import VendorCreate, VendorRead
from app.models.vendor import Vendor

router = APIRouter()

@router.post("/", response_model=VendorRead)
def create_vendor(data: VendorCreate, session: Session = Depends(get_session)):
    vendor = Vendor(name=data.name, category=data.category)
    session.add(vendor)
    session.commit()
    session.refresh(vendor)
    return vendor

@router.get("/{vendor_id}", response_model=VendorRead)
def get_vendor(vendor_id: int, session: Session = Depends(get_session)):
    vendor = session.get(Vendor, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor
