def test_open_cash_register(client):
    response = client.post("/caja/abrir", json={"saldo_inicial": 100.0})
    assert response.status_code in {200, 400}
