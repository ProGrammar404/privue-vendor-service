from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.core.database import get_session
from app.models.vendor import Vendor
from app.models.score import VendorScore
from app.schemas.score import ScoreRead, ScoreHistoryResponse

router = APIRouter()

@router.get("/{vendor_id}", response_model=ScoreHistoryResponse)
def get_score_history(
    vendor_id: int,
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session)
):
    vendor = session.get(Vendor, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    count_query = select(VendorScore).where(VendorScore.vendor_id == vendor_id)
    count = session.exec(count_query).all()
    total_count = len(count)

    query = (
        select(VendorScore)
        .where(VendorScore.vendor_id == vendor_id)
        .order_by(VendorScore.calculated_at.desc())
        .limit(limit)
        .offset(offset)
    )
    results = session.exec(query).all()

    scores = [
        ScoreRead(score=row.score, calculated_at=row.calculated_at)
        for row in results
    ]

    return ScoreHistoryResponse(total=total_count, items=scores)
