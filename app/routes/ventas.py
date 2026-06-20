from typing import List

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.schemas.schemas import VentaCreate
from app.schemas.schemas import VentaResponse

from app.services.venta_service import VentaService

from app.utils.dependencies import get_db

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