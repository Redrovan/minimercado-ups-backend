import pytest

def test_proveedores_crud(client):
    # 1. Create supplier
    create_payload = {
    "ruc": "1712345678001",
    "nombre": "Distribuidora La Favorita",
    "telefono": "022999999",
    "correo": "contacto@lafavorita.com",
    "activo": True
    }
    response = client.post("/proveedores", json=create_payload)
    assert response.status_code == 200
    prov = response.json()
    assert prov["ruc"] == "1712345678001"
    assert prov["nombre"] == "Distribuidora La Favorita"
    proveedor_id = prov["id"]

    # 2. Get supplier by id
    response_get = client.get(f"/proveedores/{proveedor_id}")
    assert response_get.status_code == 200
    assert response_get.json()["nombre"] == "Distribuidora La Favorita"

    # 3. Get non-existent supplier -> raises ProveedorNoEncontrado (returns 400)
    response_get_fail = client.get("/proveedores/99999")
    assert response_get_fail.status_code == 400
    assert "Proveedor no encontrado" in response_get_fail.json()["message"]

    # 4. Update supplier
    update_payload = {
    "ruc": "1712345678001",
    "nombre": "La Favorita S.A.",
    "telefono": "022888888",
    "correo": "ventas@lafavorita.com",
    "activo": True
    }
    response_put = client.put(f"/proveedores/{proveedor_id}", json=update_payload)
    assert response_put.status_code == 200
    assert response_put.json()["nombre"] == "La Favorita S.A."

    # 5. List and search suppliers
    response_list = client.get("/proveedores?nombre=Favorita&correo=ventas")
    assert response_list.status_code == 200
    res = response_list.json()
    assert res["total"] >= 1
    assert res["items"][0]["nombre"] == "La Favorita S.A."

    # 6. Delete supplier
    response_del = client.delete(f"/proveedores/{proveedor_id}")
    assert response_del.status_code == 200

    # 7. Verify is deactivated by getting it again
    response_get_deactivated = client.get(f"/proveedores/{proveedor_id}")
    assert response_get_deactivated.status_code == 400
