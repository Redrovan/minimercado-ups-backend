from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.models.models import Producto
from app.utils.dependencies import get_db

router = APIRouter(
    prefix="/inventario",
    tags=["Inventario"]
)

@router.get("")
def inventario(
    db: Session = Depends(get_db)
):

    productos = db.query(Producto).all()

    resultado = []

    for p in productos:

        resultado.append({
            "id": p.id,
            "nombre": p.nombre,
            "stock": p.stock,
            "stock_bajo": p.stock < 10
        })

    return resultado