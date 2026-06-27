import pytest

def test_inventario_flow(client):
    # 1. Create a product first
    prod_payload = {
        "codigo_barras": "1111111111",
        "nombre": "Aceite",
        "categoria": "Comestibles",
        "costo": 2.0,
        "precio": 2.50,
        "stock": 10,
        "activo": True
    }
    response_prod = client.post("/productos", json=prod_payload)
    assert response_prod.status_code == 200
    prod = response_prod.json()
    prod_id = prod["id"]

    # 2. Consult inventory
    response_inv = client.get("/inventario")
    assert response_inv.status_code == 200
    inv = response_inv.json()
    assert len(inv) >= 1
    assert any(item["id"] == prod_id and item["stock"] == 10 for item in inv)

    # 3. Register movement: INGRESO
    mov_ingreso = {
        "producto_id": prod_id,
        "tipo_movimiento": "INGRESO",
        "cantidad": 5,
        "motivo": "Compra a proveedor"
    }
    response_mov = client.post("/inventario/movimientos", json=mov_ingreso)
    assert response_mov.status_code == 200
    assert response_mov.json()["cantidad"] == 5

    # Verify stock updated to 15
    response_get = client.get(f"/productos/{prod_id}")
    assert response_get.json()["stock"] == 15

    # 4. Register movement: SALIDA
    mov_salida = {
        "producto_id": prod_id,
        "tipo_movimiento": "SALIDA",
        "cantidad": 3,
        "motivo": "Ajuste de inventario"
    }
    response_mov2 = client.post("/inventario/movimientos", json=mov_salida)
    assert response_mov2.status_code == 200

    # Verify stock updated to 12
    response_get = client.get(f"/productos/{prod_id}")
    assert response_get.json()["stock"] == 12

    # 5. Register movement: SALIDA with insufficient stock
    mov_insufficient = {
        "producto_id": prod_id,
        "tipo_movimiento": "SALIDA",
        "cantidad": 100,
        "motivo": "Ajuste grande"
    }
    response_fail1 = client.post("/inventario/movimientos", json=mov_insufficient)
    assert response_fail1.status_code == 500  # unhandled ValueError

    # 6. Register movement: non-existent product
    mov_non_existent = {
        "producto_id": 99999,
        "tipo_movimiento": "INGRESO",
        "cantidad": 5,
        "motivo": "Ajuste"
    }
    response_fail2 = client.post("/inventario/movimientos", json=mov_non_existent)
    assert response_fail2.status_code == 500  # unhandled ValueError
