import pytest
from app.models.models import Rol

def test_usuarios_crud(client, db_session):
    # Get seeded Admin role ID
    admin_rol = db_session.query(Rol).filter(Rol.nombre == "ADMIN").first()
    assert admin_rol is not None
    rol_id = admin_rol.id

    # 1. Create a user successfully
    create_payload = {
        "username": "new_tester",
        "email": "new_tester@gmail.com",
        "password": "Password123",
        "rol_id": rol_id,
        "activo": True
    }
    response_create = client.post("/usuarios", json=create_payload)
    assert response_create.status_code == 200
    user = response_create.json()
    assert user["username"] == "new_tester"
    user_id = user["id"]

    # 2. Create user with invalid role -> fails with AppException (returns 400)
    invalid_payload = {
        "username": "invalid_user",
        "email": "invalid_user@gmail.com",
        "password": "Password123",
        "rol_id": 99999,
        "activo": True
    }
    response_invalid_role = client.post("/usuarios", json=invalid_payload)
    assert response_invalid_role.status_code == 400
    assert "Rol no encontrado" in response_invalid_role.json()["message"]

    # 3. Get user by id
    response_get = client.get(f"/usuarios/{user_id}")
    assert response_get.status_code == 200
    assert response_get.json()["username"] == "new_tester"

    # 4. Get non-existent user -> fails with UsuarioNoEncontrado (returns 400)
    response_get_fail = client.get("/usuarios/99999")
    assert response_get_fail.status_code == 400
    assert "Usuario no encontrado" in response_get_fail.json()["message"]

    # 5. List users
    response_list = client.get("/usuarios")
    assert response_list.status_code == 200
    users = response_list.json()
    assert len(users) >= 1

    # 6. Update user (without password change)
    update_payload = {
    "username": "updated_tester",
    "email": "updated_tester@gmail.com",
    "rol_id": rol_id,
    "activo": True
    }
    response_put1 = client.put(f"/usuarios/{user_id}", json=update_payload)
    assert response_put1.status_code == 200
    assert response_put1.json()["username"] == "updated_tester"

    # 7. Update user (with password change)
    update_pwd_payload = {
        "username": "updated_tester",
        "email": "updated_tester@gmail.com",
        "password": "NewPassword123",
        "rol_id": rol_id,
        "activo": True
    }
    response_put2 = client.put(f"/usuarios/{user_id}", json=update_pwd_payload)
    assert response_put2.status_code == 200

    # 8. Delete user
    response_del = client.delete(f"/usuarios/{user_id}")
    assert response_del.status_code == 200
    # User is deactivated, so its "activo" should be False
    assert response_del.json()["activo"] is False
