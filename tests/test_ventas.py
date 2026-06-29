import pytest


def test_ventas_flow(client):
    # 1. Setup client, product, open cash register

    # Create client
    res_cli = client.post(
        "/clientes",
        json={
            "cedula": "1712345678",
            "nombre": "Juan Perez",
            "telefono": "0999999999",
            "correo": "j@gmail.com"
        }
    )
    assert res_cli.status_code == 200
    cli_id = res_cli.json()["id"]

    # Create product
    res_prod = client.post(
        "/productos",
        json={
            "codigo_barras": "1111111111",
            "nombre": "Aceitito",
            "categoria": "Comida",
            "costo": 1.0,
            "precio": 2.0,
            "stock": 10
        }
    )
    assert res_prod.status_code == 200
    prod_id = res_prod.json()["id"]

    # Try creating sale before opening caja
    sale_payload = {
        "cliente_id": cli_id,
        "detalles": [
            {
                "producto_id": prod_id,
                "cantidad": 2
            }
        ]
    }

    response_no_caja = client.post("/ventas", json=sale_payload)
    assert response_no_caja.status_code == 500

    # Open caja
    res_caja = client.post(
        "/caja/abrir",
        json={"saldo_inicial": 100.0}
    )
    assert res_caja.status_code == 200
    caja_id = res_caja.json()["id"]

    # Create sale
    response_sale = client.post("/ventas", json=sale_payload)
    assert response_sale.status_code == 200

    sale = response_sale.json()

    assert sale["subtotal"] == 4.0
    assert sale["iva"] == 0.60
    assert sale["total"] == 4.60

    sale_id = sale["id"]

    # Verify stock
    res_get_prod = client.get(f"/productos/{prod_id}")
    assert res_get_prod.status_code == 200
    assert res_get_prod.json()["stock"] == 8

    # Verify caja movement
    res_movs = client.get(f"/caja/{caja_id}/movimientos")
    assert res_movs.status_code == 200
    assert len(res_movs.json()) >= 1

    # Invalid client
    fail_sale_client = {
        "cliente_id": 99999,
        "detalles": [
            {
                "producto_id": prod_id,
                "cantidad": 2
            }
        ]
    }

    res_fail1 = client.post("/ventas", json=fail_sale_client)
    assert res_fail1.status_code == 400
    assert "Cliente no encontrado" in res_fail1.json()["message"]

    # Insufficient stock
    fail_sale_stock = {
        "cliente_id": cli_id,
        "detalles": [
            {
                "producto_id": prod_id,
                "cantidad": 100
            }
        ]
    }

    res_fail2 = client.post("/ventas", json=fail_sale_stock)
    assert res_fail2.status_code == 400
    assert "Stock insuficiente" in res_fail2.json()["message"]

    # Get sale
    res_get_sale = client.get(f"/ventas/{sale_id}")
    assert res_get_sale.status_code == 200
    assert res_get_sale.json()["id"] == sale_id

    # List sales
    res_list = client.get("/ventas?cliente=Juan")
    assert res_list.status_code == 200
    assert res_list.json()["total"] >= 1

    # Update sale
    update_payload = {
        "cliente_id": cli_id,
        "detalles": [
            {
                "producto_id": prod_id,
                "cantidad": 2
            }
        ]
    }

    res_put = client.put(
        f"/ventas/{sale_id}",
        json=update_payload
    )
    assert res_put.status_code == 200

    # Delete sale
    res_del = client.delete(f"/ventas/{sale_id}")
    assert res_del.status_code == 200

    # Verify deleted
    res_get_deleted = client.get(f"/ventas/{sale_id}")
    assert res_get_deleted.status_code == 400