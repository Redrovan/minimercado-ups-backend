import pytest

def test_roles_crud(client):
    # 1. List roles (should contain ADMIN, CAJERO, VENTAS from seed)
    response_list = client.get("/roles")
    assert response_list.status_code == 200
    roles = response_list.json()
    assert len(roles) >= 3
    assert any(r["nombre"] == "ADMIN" for r in roles)

    # 2. Create new role
    create_payload = {
        "nombre": "INVITADO",
        "descripcion": "Acceso de lectura únicamente"
    }
    response_create = client.post("/roles", json=create_payload)
    assert response_create.status_code == 200
    rol = response_create.json()
    assert rol["nombre"] == "INVITADO"
    rol_id = rol["id"]

    # 3. Create existing role -> fails with AppException (returns 400)
    response_dup = client.post("/roles", json=create_payload)
    assert response_dup.status_code == 400
    assert "El rol ya existe" in response_dup.json()["message"]

    # 4. Update role
    update_payload = {
        "nombre": "INVITADO_EDITADO",
        "descripcion": "Acceso limitado"
    }
    response_put = client.put(f"/roles/{rol_id}", json=update_payload)
    assert response_put.status_code == 200
    assert response_put.json()["nombre"] == "INVITADO_EDITADO"

    # 5. Delete (deactivate) role
    response_del = client.delete(f"/roles/{rol_id}")
    assert response_del.status_code == 200
    assert response_del.json()["activo"] is False
