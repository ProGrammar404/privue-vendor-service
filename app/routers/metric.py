from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import datetime, timezone
from app.core.database import get_session
from app.schemas.metric import MetricCreate
from app.models.metric import VendorMetric
from app.models.vendor import Vendor
from app.models.score import VendorScore
from app.services.scoring import calculate_score

router = APIRouter()

@router.post("/{vendor_id}")
def add_metric(vendor_id: int, data: MetricCreate, session: Session = Depends(get_session)):
    vendor = session.get(Vendor, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    # Save metric entry
    metric = VendorMetric(
        vendor_id=vendor_id,
        on_time_delivery_rate=data.on_time_delivery_rate,
        complaint_count=data.complaint_count,
        missing_documents=data.missing_documents,
        compliance_score=data.compliance_score,
        timestamp=data.timestamp or datetime.now(timezone.utc)
    )
    session.add(metric)

    # Calculate score
    score_value = calculate_score(
        data.on_time_delivery_rate,
        data.complaint_count,
        data.missing_documents,
        data.compliance_score
    )

    # Save score history
    score_entry = VendorScore(
        vendor_id=vendor_id,
        score=score_value,
        calculated_at=datetime.now(timezone.utc)
    )
    session.add(score_entry)

    # Update latest score on vendor
    vendor.latest_score = score_value

    session.commit()
    session.refresh(metric)
    session.refresh(vendor)

    return {
        "message": "Metric added successfully",
        "latest_score": score_value
    }
