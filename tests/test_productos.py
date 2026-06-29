import pytest

def test_productos_crud(client):
    # 1. Create product
    create_payload = {
        "codigo_barras": "9876543210",
        "nombre": "Leche Entera",
        "categoria": "Lácteos",
        "costo": 0.80,
        "precio": 1.10,
        "stock": 25,
        "activo": True
    }
    response = client.post("/productos", json=create_payload)
    assert response.status_code == 200
    prod = response.json()
    assert prod["codigo_barras"] == "9876543210"
    assert prod["nombre"] == "Leche Entera"
    product_id = prod["id"]

    # 2. Get product by id
    response_get = client.get(f"/productos/{product_id}")
    assert response_get.status_code == 200
    assert response_get.json()["nombre"] == "Leche Entera"

    # 3. Get non-existent product -> raises ProductoNoEncontrado (returns 400)
    response_get_fail = client.get("/productos/99999")
    assert response_get_fail.status_code == 400
    assert "Producto no encontrado" in response_get_fail.json()["message"]

    # 4. Update product
    update_payload = {
    "codigo_barras": "9876543210",
    "nombre": "Leche Semidescremada",
    "categoria": "Lácteos",
    "costo": 0.85,
    "precio": 1.15,
    "stock": 30,
    "activo": True
    }
    response_put = client.put(f"/productos/{product_id}", json=update_payload)
    assert response_put.status_code == 200
    assert response_put.json()["nombre"] == "Leche Semidescremada"
    assert response_put.json()["stock"] == 30

    # 5. List and filter products
    response_list = client.get("/productos?nombre=Leche&categoria=Lácteos&stock_minimo=10")
    assert response_list.status_code == 200
    res = response_list.json()
    assert res["total"] >= 1
    assert res["items"][0]["nombre"] == "Leche Semidescremada"

    # 6. Delete product
    response_del = client.delete(f"/productos/{product_id}")
    assert response_del.status_code == 200

    # 7. Verify is deactivated by getting it again
    response_get_deactivated = client.get(f"/productos/{product_id}")
    assert response_get_deactivated.status_code == 400
