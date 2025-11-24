MAX_COMPLAINTS = 10  # threshold where complaint impact becomes max penalty

def calculate_score(on_time_delivery_rate: float,
                    complaint_count: int,
                    missing_documents: bool,
                    compliance_score: float) -> float:

    # Normalize complaints (higher complaints => worse)
    complaint_normalized = max(0.0, 1 - (complaint_count / MAX_COMPLAINTS))
    complaint_score = complaint_normalized * 100  # 0–100 scale

    score = (
        0.4 * on_time_delivery_rate +
        0.4 * compliance_score +
        0.1 * complaint_score -
        (10 if missing_documents else 0)
    )

    # Clamp and round to 2 decimals
    return round(max(0.0, min(100.0, score)), 2)
