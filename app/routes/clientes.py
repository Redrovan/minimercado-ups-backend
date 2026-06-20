from typing import List

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.schemas.schemas import ClienteCreate
from app.schemas.schemas import ClienteResponse

from app.services.cliente_service import ClienteService

from app.utils.dependencies import get_db

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