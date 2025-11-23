from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from datetime import datetime, timezone

from app.core.database import get_session
from app.models.vendor import Vendor
from app.models.metric import VendorMetric
from app.models.score import VendorScore
from app.services.scoring import calculate_score

router = APIRouter()

@router.post("/recompute-scores")
def recompute_scores(session: Session = Depends(get_session)):
    vendors = session.exec(select(Vendor)).all()
    updated = 0

    for vendor in vendors:
        # get latest metric by timestamp
        metric = (
            session.exec(
                select(VendorMetric)
                .where(VendorMetric.vendor_id == vendor.id)
                .order_by(VendorMetric.timestamp.desc())
            ).first()
        )

        if not metric:
            continue

        new_score = calculate_score(
            metric.on_time_delivery_rate,
            metric.complaint_count,
            metric.missing_documents,
            metric.compliance_score
        )

        # create history entry
        new_score_entry = VendorScore(
            vendor_id=vendor.id,
            score=new_score,
            calculated_at=datetime.now(timezone.utc)
        )
        session.add(new_score_entry)

        # update vendor
        vendor.latest_score = new_score
        updated += 1

    session.commit()

    return {
        "message": "Recomputation complete",
        "vendors_updated": updated
    }
