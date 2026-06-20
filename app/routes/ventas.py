from typing import List

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.schemas.schemas import VentaCreate
from app.schemas.schemas import VentaResponse

from app.services.venta_service import VentaService

from app.utils.dependencies import get_db

from app.schemas.schemas import VentaUpdate

router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"]
)

service = VentaService()


@router.get(
    "",
    response_model=List[VentaResponse]
)
def listar(
    db: Session = Depends(get_db)
):

    return service.listar(db)


@router.post(
    "",
    response_model=VentaResponse
)
def crear(
    payload: VentaCreate,
    db: Session = Depends(get_db)
):

    return service.crear(db, payload)

@router.get(
    "/{venta_id}",
    response_model=VentaResponse
)
def obtener_venta(
    venta_id: int,
    db: Session = Depends(get_db)
):

    return service.obtener_por_id(
        db,
        venta_id
    )


@router.put(
    "/{venta_id}",
    response_model=VentaResponse
)
def actualizar_venta(
    venta_id: int,
    payload: VentaUpdate,
    db: Session = Depends(get_db)
):

    return service.actualizar(
        db,
        venta_id,
        payload
    )


@router.delete(
    "/{venta_id}"
)
def eliminar_venta(
    venta_id: int,
    db: Session = Depends(get_db)
):

    return service.eliminar(
        db,
        venta_id
    )