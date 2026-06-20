from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas.schemas import PageResponse, ProductoCreate, ProductoResponse, ProductoUpdate
from app.services.producto_service import ProductoService
from app.utils.dependencies import get_db

router = APIRouter(prefix="/productos", tags=["Productos"])
service = ProductoService()


@router.get("", response_model=PageResponse[ProductoResponse], summary="Listar productos")
def listar(db: Session = Depends(get_db), page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), nombre: str | None = None, categoria: str | None = None, stock_minimo: int | None = Query(default=None, ge=0)):
    return service.listar(db, page=page, size=size, nombre=nombre, categoria=categoria, stock_minimo=stock_minimo)


@router.post("", response_model=ProductoResponse, summary="Crear producto")
def crear(payload: ProductoCreate, db: Session = Depends(get_db)):
    return service.crear(db, payload)

@router.get("/{producto_id}", response_model=ProductoResponse, summary="Obtener producto")
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    return service.obtener_por_id(db, producto_id)


@router.delete("/{producto_id}", summary="Desactivar producto")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    return service.eliminar(db, producto_id)

@router.put("/{producto_id}", response_model=ProductoResponse, summary="Actualizar producto")
def actualizar_producto(producto_id: int, payload: ProductoUpdate, db: Session = Depends(get_db)):
    return service.actualizar(db, producto_id, payload)