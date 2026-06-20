from pydantic import BaseModel
from datetime import datetime

class ProductoCreate(BaseModel):

    codigo_barras: str
    nombre: str
    categoria: str
    costo: float
    precio: float
    stock: int


class ProductoResponse(ProductoCreate):

    id: int

    class Config:
        from_attributes = True


# ======================
# CLIENTES
# ======================

class ClienteCreate(BaseModel):

    cedula: str
    nombre: str
    telefono: str
    correo: str


class ClienteResponse(ClienteCreate):

    id: int

    class Config:
        from_attributes = True


# ======================
# PROVEEDORES
# ======================

class ProveedorCreate(BaseModel):

    ruc: str
    nombre: str
    telefono: str
    correo: str


class ProveedorResponse(ProveedorCreate):

    id: int

    class Config:
        from_attributes = True


class VentaCreate(BaseModel):

    cliente_id: int
    total: float


class VentaResponse(BaseModel):

    id: int
    cliente_id: int
    total: float
    fecha: datetime

    class Config:
        from_attributes = True

class ProductoUpdate(BaseModel):

    codigo_barras: str
    nombre: str
    categoria: str
    costo: float
    precio: float
    stock: int

class ClienteUpdate(BaseModel):

    cedula: str
    nombre: str
    telefono: str
    correo: str

class ProveedorUpdate(BaseModel):

    ruc: str
    nombre: str
    telefono: str
    correo: str