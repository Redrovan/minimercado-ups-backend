from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import Base
from app.database import engine
from app.exceptions import AppException
from app.models.models import Rol
from app.models.models import Usuario
from app.routes.auth import router as auth_router
from app.routes.caja import router as caja_router
from app.routes.clientes import router as cliente_router
from app.routes.inventario import router as inventario_router
from app.routes.productos import router as producto_router
from app.routes.proveedores import router as proveedor_router
from app.routes.reportes import router as reportes_router
from app.routes.roles import router as rol_router
from app.routes.usuarios import router as usuario_router
from app.routes.ventas import router as venta_router
from app.security import hash_password
from app.utils.dependencies import get_db


app = FastAPI(title="Minimercado UPS", version="2.0.0")


def seed_defaults(db: Session) -> None:
    roles = {
        "ADMIN": "Administrador del sistema",
        "CAJERO": "Operación de caja y ventas",
        "VENTAS": "Registro de ventas",
    }
    for nombre, descripcion in roles.items():
        existing_role = db.query(Rol).filter(Rol.nombre == nombre).first()
        if not existing_role:
            db.add(Rol(nombre=nombre, descripcion=descripcion))
    db.flush()

    existing_admin = db.query(Usuario).filter(Usuario.username == "admin").first()
    admin_role = db.query(Rol).filter(Rol.nombre == "ADMIN").first()
    if admin_role and not existing_admin:
        db.add(
            Usuario(
                username="admin",
                email="admin@minimercado.com",
                password_hash=hash_password("Admin12345"),
                rol_id=admin_role.id,
            )
        )
    db.commit()


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        seed_defaults(db)
    finally:
        db.close()


@app.exception_handler(AppException)
def handle_app_exception(_, exc: AppException):
    return JSONResponse(status_code=400, content={"success": False, "message": exc.message})


@app.exception_handler(RequestValidationError)
def handle_validation_exception(_, exc: RequestValidationError):
    message = exc.errors()[0]["msg"] if exc.errors() else "Error de validación"
    return JSONResponse(status_code=422, content={"success": False, "message": message})


@app.get("/")
def root():
    return {"mensaje": "Backend Minimercado UPS"}


app.include_router(auth_router)
app.include_router(rol_router)
app.include_router(usuario_router)
app.include_router(producto_router)
app.include_router(cliente_router)
app.include_router(proveedor_router)
app.include_router(venta_router)
app.include_router(caja_router)
app.include_router(inventario_router)
app.include_router(reportes_router)