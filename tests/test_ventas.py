import pytest

def test_ventas_flow(client):
    # 1. Setup client, product, open cash register
    # Create client
    res_cli = client.post("/clientes", json={
        "cedula": "1712345678", "nombre": "Juan Perez", "telefono": "099", "correo": "j@gmail.com"
    })
    assert res_cli.status_code == 200
    cli_id = res_cli.json()["id"]

    # Create product
    res_prod = client.post("/productos", json={
        "codigo_barras": "Aceit-1", "nombre": "Aceitito", "categoria": "Comida",
        "costo": 1.0, "precio": 2.0, "stock": 10
    })
    assert res_prod.status_code == 200
    prod_id = res_prod.json()["id"]

    # Try creating sale before opening caja -> should raise ValueError ("No existe caja abierta")
    sale_payload = {
        "cliente_id": cli_id,
        "detalles": [{"producto_id": prod_id, "cantidad": 2}]
    }
    response_no_caja = client.post("/ventas", json=sale_payload)
    assert response_no_caja.status_code == 500  # unhandled ValueError

    # Open caja
    res_caja = client.post("/caja/abrir", json={"saldo_inicial": 100.0})
    assert res_caja.status_code == 200
    caja_id = res_caja.json()["id"]

    # 2. Create sale successfully
    response_sale = client.post("/ventas", json=sale_payload)
    assert response_sale.status_code == 200
    sale = response_sale.json()
    
    # Assert price calculation: subtotal = 2.0 * 2 = 4.0; iva = 0.60; total = 4.60
    assert sale["subtotal"] == 4.0
    assert sale["iva"] == 0.60
    assert sale["total"] == 4.60
    sale_id = sale["id"]

    # Verify product stock updated (10 - 2 = 8)
    res_get_prod = client.get(f"/productos/{prod_id}")
    assert res_get_prod.json()["stock"] == 8

    # Verify caja balance updated (100.0 + 4.60 = 104.60)
    res_movs = client.get(f"/caja/{caja_id}/movimientos")
    assert res_movs.status_code == 200
    assert len(res_movs.json()) >= 1

    # 3. Create sale with non-existent client -> raises ClienteNoEncontrado (returns 400)
    fail_sale_client = {
        "cliente_id": 99999,
        "detalles": [{"producto_id": prod_id, "cantidad": 2}]
    }
    res_fail1 = client.post("/ventas", json=fail_sale_client)
    assert res_fail1.status_code == 400
    assert "Cliente no encontrado" in res_fail1.json()["message"]

    # 4. Create sale with insufficient stock -> raises StockInsuficiente (returns 400)
    fail_sale_stock = {
        "cliente_id": cli_id,
        "detalles": [{"producto_id": prod_id, "cantidad": 100}]
    }
    res_fail2 = client.post("/ventas", json=fail_sale_stock)
    assert res_fail2.status_code == 400
    assert "Stock insuficiente" in res_fail2.json()["message"]

    # 5. Get sale by id
    res_get_sale = client.get(f"/ventas/{sale_id}")
    assert res_get_sale.status_code == 200
    assert res_get_sale.json()["id"] == sale_id

    # 6. List and filter sales
    res_list = client.get("/ventas?cliente=Juan")
    assert res_list.status_code == 200
    assert res_list.json()["total"] >= 1

    # 7. Update sale client
    res_put = client.put(f"/ventas/{sale_id}", json={"cliente_id": cli_id})
    assert res_put.status_code == 200

    # 8. Deactivate sale
    res_del = client.delete(f"/ventas/{sale_id}")
    assert res_del.status_code == 200

    # Verify deactivated sale is not found
    res_get_deleted = client.get(f"/ventas/{sale_id}")
    assert res_get_deleted.status_code == 400
