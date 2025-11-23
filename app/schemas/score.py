from typing import List
from datetime import datetime
from sqlmodel import SQLModel

class ScoreRead(SQLModel):
    score: float
    calculated_at: datetime

class ScoreHistoryResponse(SQLModel):
    total: int
    items: List[ScoreRead]
