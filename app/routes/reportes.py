from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.models import Cliente
from app.models.models import DetalleVenta
from app.models.models import Producto
from app.models.models import Proveedor
from app.models.models import Venta
from app.schemas.schemas import InventarioResponse
from app.schemas.schemas import ProductosMasVendidosResponse
from app.schemas.schemas import ResumenReportResponse
from app.schemas.schemas import StockBajoResponse
from app.schemas.schemas import TopClientesResponse
from app.schemas.schemas import VentasPorMesResponse
from app.utils.dependencies import get_db

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/resumen", response_model=ResumenReportResponse)
def resumen(db: Session = Depends(get_db)):
    return ResumenReportResponse(
        productos=db.query(Producto).filter(Producto.activo.is_(True)).count(),
        clientes=db.query(Cliente).filter(Cliente.activo.is_(True)).count(),
        proveedores=db.query(Proveedor).filter(Proveedor.activo.is_(True)).count(),
        ventas=db.query(Venta).filter(Venta.activo.is_(True)).count(),
        ingresos=db.query(func.coalesce(func.sum(Venta.total), 0)).scalar() or 0,
    )


@router.get("/productos-mas-vendidos", response_model=list[ProductosMasVendidosResponse])
def productos_mas_vendidos(db: Session = Depends(get_db)):
    rows = (
        db.query(
            Producto.id.label("producto_id"),
            Producto.nombre.label("nombre"),
            func.sum(DetalleVenta.cantidad).label("cantidad_vendida"),
            func.sum(DetalleVenta.subtotal).label("total_vendido"),
        )
        .join(DetalleVenta, DetalleVenta.producto_id == Producto.id)
        .group_by(Producto.id, Producto.nombre)
        .order_by(func.sum(DetalleVenta.cantidad).desc())
        .all()
    )
    return [ProductosMasVendidosResponse(**row._asdict()) for row in rows]


@router.get("/stock-bajo", response_model=list[StockBajoResponse])
def stock_bajo(db: Session = Depends(get_db)):
    rows = db.query(Producto).filter(Producto.activo.is_(True), Producto.stock < 10).all()
    return [StockBajoResponse(id=row.id, nombre=row.nombre, stock=row.stock) for row in rows]


@router.get("/ventas-por-mes", response_model=list[VentasPorMesResponse])
def ventas_por_mes(db: Session = Depends(get_db)):
    rows = (
        db.query(
            func.strftime("%Y-%m", Venta.fecha).label("mes"),
            func.count(Venta.id).label("total_ventas"),
            func.coalesce(func.sum(Venta.total), 0).label("ingresos"),
        )
        .group_by(func.strftime("%Y-%m", Venta.fecha))
        .order_by(func.strftime("%Y-%m", Venta.fecha))
        .all()
    )
    return [VentasPorMesResponse(**row._asdict()) for row in rows]


@router.get("/top-clientes", response_model=list[TopClientesResponse])
def top_clientes(db: Session = Depends(get_db)):
    rows = (
        db.query(
            Cliente.id.label("cliente_id"),
            Cliente.nombre.label("nombre"),
            func.count(Venta.id).label("total_compras"),
            func.coalesce(func.sum(Venta.total), 0).label("total_gastado"),
        )
        .join(Venta, Venta.cliente_id == Cliente.id)
        .group_by(Cliente.id, Cliente.nombre)
        .order_by(func.sum(Venta.total).desc())
        .all()
    )
    return [TopClientesResponse(**row._asdict()) for row in rows]


@router.get("/inventario", response_model=list[InventarioResponse])
def inventario(db: Session = Depends(get_db)):
    rows = db.query(Producto).filter(Producto.activo.is_(True)).all()
    return [
        InventarioResponse(id=row.id, nombre=row.nombre, categoria=row.categoria, stock=row.stock, precio=row.precio, costo=row.costo, activo=row.activo)
        for row in rows
    ]