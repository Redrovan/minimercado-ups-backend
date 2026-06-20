from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas.schemas import ClienteCreate, ClienteResponse, ClienteUpdate, PageResponse
from app.services.cliente_service import ClienteService
from app.utils.dependencies import get_db

router = APIRouter(prefix="/clientes", tags=["Clientes"])
service = ClienteService()


@router.get("", response_model=PageResponse[ClienteResponse], summary="Listar clientes")
def listar(db: Session = Depends(get_db), page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), nombre: str | None = None, correo: str | None = None):
    return service.listar(db, page=page, size=size, nombre=nombre, correo=correo)


@router.post("", response_model=ClienteResponse, summary="Crear cliente")
def crear(payload: ClienteCreate, db: Session = Depends(get_db)):
    return service.crear(db, payload)

@router.get("/{cliente_id}", response_model=ClienteResponse, summary="Obtener cliente")
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return service.obtener_por_id(db, cliente_id)


@router.put("/{cliente_id}", response_model=ClienteResponse, summary="Actualizar cliente")
def actualizar_cliente(cliente_id: int, payload: ClienteUpdate, db: Session = Depends(get_db)):
    return service.actualizar(db, cliente_id, payload)


@router.delete("/{cliente_id}", summary="Desactivar cliente")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return service.eliminar(db, cliente_id)