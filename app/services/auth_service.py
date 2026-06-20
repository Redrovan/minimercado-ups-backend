from fastapi import HTTPException

from app.repositories.usuario_repository import UsuarioRepository
from app.security import create_access_token
from app.security import create_refresh_token
from app.security import decode_token
from app.security import verify_password


repo = UsuarioRepository()


class AuthService:
    def login(self, db, payload):
        usuario = repo.obtener_por_username_o_email(db, payload.username_or_email)
        if not usuario or not usuario.activo:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        if not verify_password(payload.password, usuario.password_hash):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        return {
            "access_token": create_access_token(str(usuario.id)),
            "refresh_token": create_refresh_token(str(usuario.id)),
            "token_type": "bearer",
        }

    def refresh(self, payload):
        token_data = decode_token(payload.refresh_token)
        if token_data.get("type") != "refresh" or not token_data.get("sub"):
            raise HTTPException(status_code=401, detail="Refresh token inválido")
        subject = str(token_data["sub"])
        return {
            "access_token": create_access_token(subject),
            "refresh_token": create_refresh_token(subject),
            "token_type": "bearer",
        }
