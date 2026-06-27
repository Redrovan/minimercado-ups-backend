import pytest

def test_reportes_endpoints(client):
    # 1. Setup entities (Client, Product with low stock, Product with high stock, Supplier)
    # Create client
    res_cli = client.post("/clientes", json={
        "cedula": "1712345678", "nombre": "Juan Perez", "telefono": "099", "correo": "j@gmail.com"
    })
    cli_id = res_cli.json()["id"]

    # Create supplier
    res_prov = client.post("/proveedores", json={
        "ruc": "1712345678001", "nombre": "Prov", "telefono": "099", "correo": "p@gmail.com", "direccion": "Quito"
    })

    # Create product with low stock (< 10)
    res_prod1 = client.post("/productos", json={
        "codigo_barras": "aceite", "nombre": "Aceite", "categoria": "Comida",
        "costo": 1.0, "precio": 2.0, "stock": 5
    })
    prod1_id = res_prod1.json()["id"]

    # Create product with high stock (>= 10)
    res_prod2 = client.post("/productos", json={
        "codigo_barras": "arroz", "nombre": "Arroz", "categoria": "Comida",
        "costo": 0.5, "precio": 1.0, "stock": 50
    })

    # 2. Open register and record a sale
    client.post("/caja/abrir", json={"saldo_inicial": 100.0})
    client.post("/ventas", json={
        "cliente_id": cli_id,
        "detalles": [{"producto_id": prod1_id, "cantidad": 2}]
    })

    # 3. Test /reportes/resumen
    res = client.get("/reportes/resumen")
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["productos"] == 2
    assert res_json["clientes"] == 1
    assert res_json["proveedores"] == 1
    assert res_json["ventas"] == 1
    assert res_json["ingresos"] > 0.0

    # 4. Test /reportes/productos-mas-vendidos
    res_top_prod = client.get("/reportes/productos-mas-vendidos")
    assert res_top_prod.status_code == 200
    assert len(res_top_prod.json()) >= 1
    assert res_top_prod.json()[0]["producto_id"] == prod1_id

    # 5. Test /reportes/stock-bajo
    res_low_stock = client.get("/reportes/stock-bajo")
    assert res_low_stock.status_code == 200
    low_stock_ids = [item["id"] for item in res_low_stock.json()]
    assert prod1_id in low_stock_ids  # oil should be low stock (stock was 5, after selling 2 it's 3)

    # 6. Test /reportes/ventas-por-mes
    res_sales_month = client.get("/reportes/ventas-por-mes")
    assert res_sales_month.status_code == 200
    assert len(res_sales_month.json()) >= 1

    # 7. Test /reportes/top-clientes
    res_top_cli = client.get("/reportes/top-clientes")
    assert res_top_cli.status_code == 200
    assert len(res_top_cli.json()) >= 1
    assert res_top_cli.json()[0]["cliente_id"] == cli_id

    # 8. Test /reportes/inventario
    res_inv = client.get("/reportes/inventario")
    assert res_inv.status_code == 200
    assert len(res_inv.json()) >= 2
