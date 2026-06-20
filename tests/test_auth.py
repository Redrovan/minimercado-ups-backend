from app.models.models import Rol
from app.models.models import Usuario
from app.security import hash_password


def test_login_returns_tokens(client, db_session):
    rol = Rol(nombre="TEST", descripcion="Rol de prueba")
    db_session.add(rol)
    db_session.commit()
    usuario = Usuario(username="tester", email="tester@example.com", password_hash=hash_password("Password123"), rol_id=rol.id)
    db_session.add(usuario)
    db_session.commit()

    response = client.post("/auth/login", json={"username_or_email": "tester", "password": "Password123"})
    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["refresh_token"]
