from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.routes.productos import router as producto_router

from app.routes.clientes import router as cliente_router
from app.routes.proveedores import router as proveedor_router

from app.routes.ventas import router as venta_router

from app.routes.inventario import router as inventario_router
from app.routes.reportes import router as reportes_router

app = FastAPI(
    title="Minimercado UPS"
)

Base.metadata.create_all(bind=engine)

app.include_router(producto_router)
app.include_router(cliente_router)
app.include_router(proveedor_router)
app.include_router(venta_router)
app.include_router(inventario_router)
app.include_router(reportes_router)

@app.get("/")
def root():

    return {
        "mensaje": "Backend Minimercado UPS"
    }