def test_create_client(client):
    response = client.post(
        "/clientes",
        json={
            "cedula": "1234567890",
            "nombre": "Juan Perez",
            "telefono": "0987654321",
            "correo": "juan@example.com",
            "activo": True,
        },
    )
    assert response.status_code == 200
