from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.schemas import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.services.usuario_service import UsuarioService
from app.utils.dependencies import get_db

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
service = UsuarioService()


@router.get("", response_model=list[UsuarioResponse])
def listar(db: Session = Depends(get_db)):
    return service.listar(db)


@router.post("", response_model=UsuarioResponse)
def crear(payload: UsuarioCreate, db: Session = Depends(get_db)):
    return service.crear(db, payload)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener(usuario_id: int, db: Session = Depends(get_db)):
    return service.obtener_por_id(db, usuario_id)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar(usuario_id: int, payload: UsuarioUpdate, db: Session = Depends(get_db)):
    return service.actualizar(db, usuario_id, payload)


@router.delete("/{usuario_id}")
def eliminar(usuario_id: int, db: Session = Depends(get_db)):
    return service.eliminar(db, usuario_id)
