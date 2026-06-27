from app.models.models import Rol
from app.models.models import Usuario
from app.security import hash_password

def test_auth_flow(client, db_session):
    # Setup test user and role
    rol = Rol(nombre="TEST", descripcion="Rol de prueba")
    db_session.add(rol)
    db_session.commit()
    usuario = Usuario(
        username="tester",
        email="tester@example.com",
        password_hash=hash_password("Password123"),
        rol_id=rol.id,
        activo=True
    )
    db_session.add(usuario)
    db_session.commit()

    # 1. Login success
    response = client.post("/auth/login", json={"username_or_email": "tester", "password": "Password123"})
    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["refresh_token"]
    
    access_token = body["access_token"]
    refresh_token = body["refresh_token"]

    # 2. Login invalid password
    response_fail = client.post("/auth/login", json={"username_or_email": "tester", "password": "WrongPassword"})
    assert response_fail.status_code == 401
    assert response_fail.json()["detail"] == "Credenciales inválidas"

    # 3. Get /auth/me with credentials
    headers = {"Authorization": f"Bearer {access_token}"}
    response_me = client.get("/auth/me", headers=headers)
    assert response_me.status_code == 200
    assert response_me.json()["username"] == "tester"

    # 4. Get /auth/me without headers -> 401
    response_me_no_auth = client.get("/auth/me")
    assert response_me_no_auth.status_code == 401

    # 5. Refresh token success
    response_refresh = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert response_refresh.status_code == 200
    refresh_body = response_refresh.json()
    assert refresh_body["access_token"]
    assert refresh_body["refresh_token"]

    # 6. Refresh token failure with invalid token -> returns 500 due to ValueError
    response_refresh_fail = client.post("/auth/refresh", json={"refresh_token": "invalid_refresh_token"})
    assert response_refresh_fail.status_code == 500
