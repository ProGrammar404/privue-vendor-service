def test_create_vendor(client):
    response = client.post("/vendors/", json={
        "name": "Test Vendor",
        "category": "supplier"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Vendor"
    assert data["latest_score"] is None


def test_get_vendor(client):
    create_res = client.post("/vendors/", json={
        "name": "Vendor 2",
        "category": "dealer"
    })
    vendor_id = create_res.json()["id"]

    get_res = client.get(f"/vendors/{vendor_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == vendor_id
