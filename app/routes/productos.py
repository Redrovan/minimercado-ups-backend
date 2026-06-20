from typing import List

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.schemas.schemas import ProductoCreate
from app.schemas.schemas import ProductoResponse

from app.services.producto_service import ProductoService

from app.utils.dependencies import get_db

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

service = ProductoService()


@router.get(
    "",
    response_model=List[ProductoResponse]
)
def listar(
    db: Session = Depends(get_db)
):

    return service.listar(db)


@router.post(
    "",
    response_model=ProductoResponse
)
def crear(
    payload: ProductoCreate,
    db: Session = Depends(get_db)
):

    return service.crear(db, payload)