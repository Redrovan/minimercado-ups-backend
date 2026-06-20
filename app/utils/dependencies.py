from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.models import Usuario
from app.security import ALGORITHM
from app.security import SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject = payload.get("sub")
        token_type = payload.get("type")
        if not subject or token_type != "access":
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    usuario = db.query(Usuario).filter(Usuario.id == int(subject), Usuario.activo.is_(True)).first()
    if not usuario:
        raise credentials_exception
    return usuario


def require_roles(*roles: str):
    def dependency(usuario=Depends(get_current_user)):
        if usuario.rol.nombre not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para ejecutar esta acción",
            )
        return usuario

    return dependency