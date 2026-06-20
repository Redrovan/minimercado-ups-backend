from typing import List

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.schemas.schemas import ProveedorCreate
from app.schemas.schemas import ProveedorResponse

from app.services.proveedor_service import ProveedorService

from app.utils.dependencies import get_db

from app.schemas.schemas import ProveedorUpdate

router = APIRouter(
    prefix="/proveedores",
    tags=["Proveedores"]
)

service = ProveedorService()


@router.get(
    "",
    response_model=List[ProveedorResponse]
)
def listar(
    db: Session = Depends(get_db)
):

    return service.listar(db)


@router.post(
    "",
    response_model=ProveedorResponse
)
def crear(
    payload: ProveedorCreate,
    db: Session = Depends(get_db)
):

    return service.crear(db, payload)

@router.get(
    "/{proveedor_id}",
    response_model=ProveedorResponse
)
def obtener_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db)
):

    return service.obtener_por_id(
        db,
        proveedor_id
    )


@router.put(
    "/{proveedor_id}",
    response_model=ProveedorResponse
)
def actualizar_proveedor(
    proveedor_id: int,
    payload: ProveedorUpdate,
    db: Session = Depends(get_db)
):

    return service.actualizar(
        db,
        proveedor_id,
        payload
    )


@router.delete(
    "/{proveedor_id}"
)
def eliminar_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db)
):

    return service.eliminar(
        db,
        proveedor_id
    )