from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas.schemas import PageResponse, ProveedorCreate, ProveedorResponse, ProveedorUpdate
from app.services.proveedor_service import ProveedorService
from app.utils.dependencies import get_db

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])
service = ProveedorService()


@router.get("", response_model=PageResponse[ProveedorResponse], summary="Listar proveedores")
def listar(db: Session = Depends(get_db), page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), nombre: str | None = None, correo: str | None = None):
    return service.listar(db, page=page, size=size, nombre=nombre, correo=correo)


@router.post("", response_model=ProveedorResponse, summary="Crear proveedor")
def crear(payload: ProveedorCreate, db: Session = Depends(get_db)):
    return service.crear(db, payload)

@router.get("/{proveedor_id}", response_model=ProveedorResponse, summary="Obtener proveedor")
def obtener_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    return service.obtener_por_id(db, proveedor_id)


@router.put("/{proveedor_id}", response_model=ProveedorResponse, summary="Actualizar proveedor")
def actualizar_proveedor(proveedor_id: int, payload: ProveedorUpdate, db: Session = Depends(get_db)):
    return service.actualizar(db, proveedor_id, payload)


@router.delete("/{proveedor_id}", summary="Desactivar proveedor")
def eliminar_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    return service.eliminar(db, proveedor_id)