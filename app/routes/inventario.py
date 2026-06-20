from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.models import MovimientoInventario
from app.models.models import Producto
from app.schemas.schemas import MovimientoInventarioCreate, MovimientoInventarioResponse
from app.schemas.schemas import InventarioResponse
from app.utils.dependencies import get_db

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.get("", response_model=list[InventarioResponse], summary="Consultar inventario")
def inventario(db: Session = Depends(get_db)):
    productos = db.query(Producto).filter(Producto.activo.is_(True)).all()
    return [
        InventarioResponse(
            id=p.id,
            nombre=p.nombre,
            categoria=p.categoria,
            stock=p.stock,
            precio=p.precio,
            costo=p.costo,
            activo=p.activo,
        )
        for p in productos
    ]


@router.post("/movimientos", response_model=MovimientoInventarioResponse, summary="Registrar movimiento de inventario")
def crear_movimiento(payload: MovimientoInventarioCreate, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == payload.producto_id, Producto.activo.is_(True)).first()
    if not producto:
        raise ValueError("Producto no encontrado")
    if payload.tipo_movimiento.upper() in {"SALIDA", "SALIDA_VENTA"} and producto.stock < payload.cantidad:
        raise ValueError("Stock insuficiente")
    if payload.tipo_movimiento.upper() in {"SALIDA", "SALIDA_VENTA"}:
        producto.stock -= payload.cantidad
    else:
        producto.stock += payload.cantidad
    movimiento = MovimientoInventario(**payload.model_dump())
    db.add(movimiento)
    db.commit()
    db.refresh(movimiento)
    return movimiento