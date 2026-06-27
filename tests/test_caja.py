import pytest

def test_caja_lifecycle(client):
    # 1. Open register
    response = client.post("/caja/abrir", json={"saldo_inicial": 150.0})
    assert response.status_code == 200
    caja = response.json()
    assert caja["estado"] == "ABIERTA"
    assert caja["saldo_inicial"] == 150.0
    caja_id = caja["id"]

    # 2. Try to open a duplicate register -> raises ValueError (500 or error)
    response_dup = client.post("/caja/abrir", json={"saldo_inicial": 200.0})
    assert response_dup.status_code == 500  # unhandled ValueError raises 500 in FastAPI by default

    # 3. Register cash movement
    movement_payload = {
        "caja_id": caja_id,
        "tipo": "INGRESO",
        "monto": 50.0,
        "descripcion": "Venta manual"
    }
    response_mov = client.post("/caja/movimientos", json=movement_payload)
    assert response_mov.status_code == 200
    mov = response_mov.json()
    assert mov["tipo"] == "INGRESO"
    assert mov["monto"] == 50.0

    # 4. List movements
    response_list = client.get(f"/caja/{caja_id}/movimientos")
    assert response_list.status_code == 200
    movs = response_list.json()
    assert len(movs) >= 1
    assert movs[0]["monto"] == 50.0

    # 5. Close register
    # Note: query parameters in FastAPI route or json? Let's check route signature:
    # @router.post("/{caja_id}/cerrar", response_model=CajaResponse)
    # def cerrar_caja(caja_id: int, saldo_final: float, db: Session = Depends(get_db)):
    # here saldo_final is a query parameter because it's not a Pydantic model
    response_close = client.post(f"/caja/{caja_id}/cerrar?saldo_final=200.0")
    assert response_close.status_code == 200
    closed_caja = response_close.json()
    assert closed_caja["estado"] == "CERRADA"
    assert closed_caja["saldo_final"] == 200.0

    # 6. Close non-existent register -> fails
    response_close_fail = client.post("/caja/99999/cerrar?saldo_final=200.0")
    assert response_close_fail.status_code == 500
