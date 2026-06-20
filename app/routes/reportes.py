from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.models import Producto
from app.models.models import Cliente
from app.models.models import Proveedor
from app.models.models import Venta

from app.utils.dependencies import get_db

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

@router.get("/resumen")
def resumen(
    db: Session = Depends(get_db)
):

    total_productos = db.query(Producto).count()

    total_clientes = db.query(Cliente).count()

    total_proveedores = db.query(Proveedor).count()

    total_ventas = db.query(Venta).count()

    ventas_generadas = (
        db.query(
            func.sum(Venta.total)
        )
        .scalar()
    )

    return {
        "productos": total_productos,
        "clientes": total_clientes,
        "proveedores": total_proveedores,
        "ventas": total_ventas,
        "ingresos": ventas_generadas or 0
    }