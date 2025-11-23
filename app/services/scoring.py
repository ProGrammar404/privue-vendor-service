def calculate_score(on_time_delivery_rate: float,
                    complaint_count: int,
                    missing_documents: bool,
                    compliance_score: float) -> float:

    score = (
        0.4 * on_time_delivery_rate +
        0.4 * compliance_score -
        0.1 * complaint_count -
        (10 if missing_documents else 0)
    )

    # Clamp between 0–100
    return max(0.0, min(100.0, score))
