def test_sales_endpoint_available(client):
    response = client.get("/ventas")
    assert response.status_code == 200
