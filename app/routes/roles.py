from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.schemas import RolCreate, RolResponse, RolUpdate
from app.services.rol_service import RolService
from app.utils.dependencies import get_db

router = APIRouter(prefix="/roles", tags=["Roles"])
service = RolService()


@router.get("", response_model=list[RolResponse])
def listar(db: Session = Depends(get_db)):
    return service.listar(db)


@router.post("", response_model=RolResponse)
def crear(payload: RolCreate, db: Session = Depends(get_db)):
    return service.crear(db, payload)


@router.put("/{rol_id}", response_model=RolResponse)
def actualizar(rol_id: int, payload: RolUpdate, db: Session = Depends(get_db)):
    return service.actualizar(db, rol_id, payload)


@router.delete("/{rol_id}", response_model=RolResponse)
def eliminar(rol_id: int, db: Session = Depends(get_db)):
    return service.eliminar(db, rol_id)
