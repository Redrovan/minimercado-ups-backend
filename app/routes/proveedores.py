from typing import List

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.schemas.schemas import ProveedorCreate
from app.schemas.schemas import ProveedorResponse

from app.services.proveedor_service import ProveedorService

from app.utils.dependencies import get_db

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