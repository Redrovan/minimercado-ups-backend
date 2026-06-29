import pytest

def test_reportes_endpoints(client):
    # 1. Crear cliente
    res_cli = client.post("/clientes", json={
        "cedula": "1712345678",
        "nombre": "Juan Perez",
        "telefono": "0999999999",
        "correo": "j@gmail.com"
    })
    assert res_cli.status_code == 200
    cli_id = res_cli.json()["id"]

    # 2. Crear proveedor
    res_prov = client.post("/proveedores", json={
        "ruc": "1712345678001",
        "nombre": "Proveedor Demo",
        "telefono": "0999999999",
        "correo": "prov@gmail.com"
    })
    assert res_prov.status_code == 200

    # 3. Crear producto con stock bajo
    res_prod1 = client.post("/productos", json={
        "codigo_barras": "10001",
        "nombre": "Aceite",
        "categoria": "Comida",
        "costo": 1.0,
        "precio": 2.0,
        "stock": 5
    })
    assert res_prod1.status_code == 200
    prod1_id = res_prod1.json()["id"]

    # 4. Crear producto con stock alto
    res_prod2 = client.post("/productos", json={
        "codigo_barras": "10002",
        "nombre": "Arroz",
        "categoria": "Comida",
        "costo": 0.5,
        "precio": 1.0,
        "stock": 50
    })
    assert res_prod2.status_code == 200

    # 5. Abrir caja
    res_caja = client.post("/caja/abrir", json={
        "saldo_inicial": 100.0
    })
    assert res_caja.status_code == 200

    # 6. Registrar venta
    res_venta = client.post("/ventas", json={
        "cliente_id": cli_id,
        "detalles": [
            {
                "producto_id": prod1_id,
                "cantidad": 2
            }
        ]
    })
    assert res_venta.status_code == 200

    # ---------------------------------------------------
    # REPORTE RESUMEN
    # ---------------------------------------------------

    res = client.get("/reportes/resumen")
    assert res.status_code == 200

    resumen = res.json()

    assert resumen["productos"] == 2
    assert resumen["clientes"] == 1
    assert resumen["proveedores"] == 1
    assert resumen["ventas"] == 1
    assert resumen["ingresos"] > 0

    # ---------------------------------------------------
    # PRODUCTOS MÁS VENDIDOS
    # ---------------------------------------------------

    res_top_prod = client.get("/reportes/productos-mas-vendidos")
    assert res_top_prod.status_code == 200

    top_prod = res_top_prod.json()

    assert len(top_prod) >= 1
    assert top_prod[0]["producto_id"] == prod1_id

    # ---------------------------------------------------
    # STOCK BAJO
    # ---------------------------------------------------

    res_stock = client.get("/reportes/stock-bajo")
    assert res_stock.status_code == 200

    stock = res_stock.json()

    assert len(stock) >= 1

    ids = [p["id"] for p in stock]

    assert prod1_id in ids

    # ---------------------------------------------------
    # VENTAS POR MES
    # ---------------------------------------------------

    res_mes = client.get("/reportes/ventas-por-mes")
    assert res_mes.status_code == 200

    ventas_mes = res_mes.json()

    assert len(ventas_mes) >= 1

    # ---------------------------------------------------
    # TOP CLIENTES
    # ---------------------------------------------------

    res_clientes = client.get("/reportes/top-clientes")
    assert res_clientes.status_code == 200

    clientes = res_clientes.json()

    assert len(clientes) >= 1
    assert clientes[0]["cliente_id"] == cli_id

    # ---------------------------------------------------
    # INVENTARIO
    # ---------------------------------------------------

    res_inv = client.get("/reportes/inventario")
    assert res_inv.status_code == 200

    inventario = res_inv.json()

    assert len(inventario) >= 2