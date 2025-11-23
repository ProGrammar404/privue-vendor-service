def test_score_history(client):
    vendor = client.post("/vendors/", json={"name": "Vendor3", "category": "supplier"}).json()
    vendor_id = vendor["id"]

    client.post(f"/metrics/{vendor_id}", json={
        "on_time_delivery_rate": 90,
        "complaint_count": 0,
        "missing_documents": False,
        "compliance_score": 85
    })

    res = client.get(f"/scores/{vendor_id}")
    assert res.status_code == 200

    data = res.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1
