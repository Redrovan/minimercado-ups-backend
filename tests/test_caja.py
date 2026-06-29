import pytest


def test_caja_lifecycle(client):
    # 1. Abrir caja
    response = client.post(
        "/caja/abrir",
        json={"saldo_inicial": 150.0}
    )

    assert response.status_code == 200

    caja = response.json()

    assert caja["estado"] == "ABIERTA"
    assert caja["saldo_inicial"] == 150.0

    caja_id = caja["id"]

    # 2. Intentar abrir otra caja
    response_dup = client.post(
        "/caja/abrir",
        json={"saldo_inicial": 200.0}
    )

    assert response_dup.status_code == 500

    # 3. Registrar movimiento
    movement_payload = {
        "caja_id": caja_id,
        "tipo_movimiento": "INGRESO",
        "monto": 50.0,
        "descripcion": "Venta manual"
    }

    response_mov = client.post(
        "/caja/movimientos",
        json=movement_payload
    )

    assert response_mov.status_code == 200

    mov = response_mov.json()

    # Mostrar la respuesta para verificar los campos
    print(mov)

    # Dependiendo del modelo puede devolver "tipo_movimiento"
    assert mov["tipo_movimiento"] == "INGRESO"
    assert mov["monto"] == 50.0

    # 4. Consultar movimientos
    response_list = client.get(f"/caja/{caja_id}/movimientos")

    assert response_list.status_code == 200

    movs = response_list.json()

    assert len(movs) >= 1
    assert movs[0]["monto"] == 50.0

    # 5. Cerrar caja
    response_close = client.post(
        f"/caja/{caja_id}/cerrar?saldo_final=200.0"
    )

    assert response_close.status_code == 200

    closed_caja = response_close.json()

    assert closed_caja["estado"] == "CERRADA"
    assert closed_caja["saldo_final"] == 200.0

    # 6. Intentar cerrar una caja inexistente
    response_close_fail = client.post(
        "/caja/99999/cerrar?saldo_final=200.0"
    )

    assert response_close_fail.status_code == 500