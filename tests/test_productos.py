def test_create_and_list_product(client):
    response = client.post(
        "/productos",
        json={
            "codigo_barras": "1234567890",
            "nombre": "Arroz",
            "categoria": "Granos",
            "costo": 1.0,
            "precio": 1.5,
            "stock": 10,
            "activo": True,
        },
    )
    assert response.status_code == 200

    list_response = client.get("/productos")
    assert list_response.status_code == 200
    assert "items" in list_response.json()
