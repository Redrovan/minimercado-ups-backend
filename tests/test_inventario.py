def test_inventory_endpoint(client):
    response = client.get("/inventario")
    assert response.status_code == 200
