
import pytest

def test_clientes_crud(client):
    # 1. Create client
    create_payload = {
        "cedula": "1712345678",
        "nombre": "Juan Perez",
        "telefono": "0999999999",
        "correo": "juan.perez@gmail.com",
        "activo": True
    }
    response = client.post("/clientes", json=create_payload)
    assert response.status_code == 200
    cli = response.json()
    assert cli["cedula"] == "1712345678"
    assert cli["nombre"] == "Juan Perez"
    cliente_id = cli["id"]

    # 2. Get client by id
    response_get = client.get(f"/clientes/{cliente_id}")
    assert response_get.status_code == 200
    assert response_get.json()["nombre"] == "Juan Perez"

    # 3. Get non-existent client -> raises ClienteNoEncontrado (returns 400)
    response_get_fail = client.get("/clientes/99999")
    assert response_get_fail.status_code == 400
    assert "Cliente no encontrado" in response_get_fail.json()["message"]

    # 4. Update client
    update_payload = {
    "cedula": "1712345678",
    "nombre": "Juan Perez Modificado",
    "telefono": "0888888888",
    "correo": "juan.modificado@gmail.com",
    "activo": True
    }
    
    response_put = client.put(f"/clientes/{cliente_id}", json=update_payload)
    assert response_put.status_code == 200
    assert response_put.json()["nombre"] == "Juan Perez Modificado"

    # 5. List and search clients
    response_list = client.get("/clientes?nombre=Perez&correo=modificado")
    assert response_list.status_code == 200
    res = response_list.json()
    assert res["total"] >= 1
    assert res["items"][0]["nombre"] == "Juan Perez Modificado"

    # 6. Delete (desactive) client
    response_del = client.delete(f"/clientes/{cliente_id}")
    assert response_del.status_code == 200

    # 7. Verify is deactivated by getting it again
    response_get_deactivated = client.get(f"/clientes/{cliente_id}")
    assert response_get_deactivated.status_code == 400
