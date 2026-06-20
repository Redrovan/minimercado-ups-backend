from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas.schemas import PageResponse, VentaCreate, VentaResponse, VentaUpdate
from app.services.venta_service import VentaService
from app.utils.dependencies import get_db

router = APIRouter(prefix="/ventas", tags=["Ventas"])
service = VentaService()


@router.get("", response_model=PageResponse[VentaResponse], summary="Listar ventas")
def listar(db: Session = Depends(get_db), page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), cliente: str | None = None, fecha_inicio: str | None = None, fecha_fin: str | None = None):
    return service.listar(db, page=page, size=size, cliente=cliente, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)


@router.post("", response_model=VentaResponse, summary="Registrar venta")
def crear(payload: VentaCreate, db: Session = Depends(get_db)):
    return service.crear(db, payload)

@router.get("/{venta_id}", response_model=VentaResponse, summary="Obtener venta")
def obtener_venta(venta_id: int, db: Session = Depends(get_db)):
    return service.obtener_por_id(db, venta_id)


@router.put("/{venta_id}", response_model=VentaResponse, summary="Actualizar venta")
def actualizar_venta(venta_id: int, payload: VentaUpdate, db: Session = Depends(get_db)):
    return service.actualizar(db, venta_id, payload)


@router.delete("/{venta_id}", summary="Desactivar venta")
def eliminar_venta(venta_id: int, db: Session = Depends(get_db)):
    return service.eliminar(db, venta_id)