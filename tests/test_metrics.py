def test_add_metric_updates_score(client):
    vendor = client.post("/vendors/", json={"name": "V1", "category": "supplier"}).json()
    vendor_id = vendor["id"]

    res = client.post(f"/metrics/{vendor_id}", json={
        "on_time_delivery_rate": 95,
        "complaint_count": 1,
        "missing_documents": False,
        "compliance_score": 90
    })

    assert res.status_code == 200
    assert "latest_score" in res.json()
    assert res.json()["latest_score"] > 0
