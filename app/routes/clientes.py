from typing import List

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.schemas.schemas import ClienteCreate
from app.schemas.schemas import ClienteResponse

from app.services.cliente_service import ClienteService

from app.utils.dependencies import get_db

from app.schemas.schemas import ClienteUpdate

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

service = ClienteService()


@router.get(
    "",
    response_model=List[ClienteResponse]
)
def listar(
    db: Session = Depends(get_db)
):

    return service.listar(db)


@router.post(
    "",
    response_model=ClienteResponse
)
def crear(
    payload: ClienteCreate,
    db: Session = Depends(get_db)
):

    return service.crear(db, payload)

@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse
)
def obtener_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):

    return service.obtener_por_id(
        db,
        cliente_id
    )


@router.put(
    "/{cliente_id}",
    response_model=ClienteResponse
)
def actualizar_cliente(
    cliente_id: int,
    payload: ClienteUpdate,
    db: Session = Depends(get_db)
):

    return service.actualizar(
        db,
        cliente_id,
        payload
    )


@router.delete(
    "/{cliente_id}"
)
def eliminar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):

    return service.eliminar(
        db,
        cliente_id
    )