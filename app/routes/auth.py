from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.schemas import CurrentUserResponse, LoginRequest, RefreshRequest, TokenResponse
from app.services.auth_service import AuthService
from app.utils.dependencies import get_current_user, get_db

router = APIRouter(prefix="/auth", tags=["Auth"])
service = AuthService()


@router.post("/login", response_model=TokenResponse, summary="Iniciar sesión")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return service.login(db, payload)


@router.post("/refresh", response_model=TokenResponse, summary="Renovar token")
def refresh(payload: RefreshRequest):
    return service.refresh(payload)


@router.get("/me", response_model=CurrentUserResponse, summary="Usuario autenticado")
def me(usuario=Depends(get_current_user)):
    return usuario
