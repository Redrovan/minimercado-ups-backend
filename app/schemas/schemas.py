from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


T = TypeVar("T")


class PageResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int


class RolBase(BaseModel):
    nombre: str = Field(min_length=3, max_length=80)
    descripcion: str | None = Field(default=None, max_length=255)


class RolCreate(RolBase):
    pass


class RolUpdate(RolBase):
    pass


class RolResponse(RolBase):
    id: int
    activo: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UsuarioBase(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    email: EmailStr
    rol_id: int = Field(gt=0)
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=8, max_length=128)


class UsuarioUpdate(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    email: EmailStr
    rol_id: int = Field(gt=0)
    activo: bool = True
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UsuarioResponse(UsuarioBase):
    id: int
    created_at: datetime
    updated_at: datetime
    rol: RolResponse | None = None
    model_config = ConfigDict(from_attributes=True)


class ProductoBase(BaseModel):
    codigo_barras: str = Field(min_length=3, max_length=80)
    nombre: str = Field(min_length=2, max_length=150)
    categoria: str = Field(min_length=2, max_length=120)
    costo: float = Field(gt=0)
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    activo: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class ProductoResponse(ProductoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ClienteBase(BaseModel):
    cedula: str = Field(min_length=10, max_length=20, pattern=r"^\d{10,20}$")
    nombre: str = Field(min_length=3, max_length=150)
    telefono: str = Field(min_length=7, max_length=20, pattern=r"^[0-9+\-()\s]{7,20}$")
    correo: EmailStr
    activo: bool = True


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ProveedorBase(BaseModel):
    ruc: str = Field(min_length=13, max_length=13, pattern=r"^\d{13}$")
    nombre: str = Field(min_length=3, max_length=150)
    telefono: str = Field(min_length=7, max_length=20, pattern=r"^[0-9+\-()\s]{7,20}$")
    correo: EmailStr
    activo: bool = True


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorUpdate(ProveedorBase):
    pass


class ProveedorResponse(ProveedorBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class VentaDetalleCreate(BaseModel):
    producto_id: int = Field(gt=0)
    cantidad: int = Field(gt=0)


class DetalleVentaResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float
    model_config = ConfigDict(from_attributes=True)


class FacturaResponse(BaseModel):
    id: int
    venta_id: int
    numero_factura: str
    fecha: datetime
    subtotal: float
    iva: float
    total: float
    model_config = ConfigDict(from_attributes=True)


class VentaCreate(BaseModel):
    cliente_id: int = Field(gt=0)
    detalles: list[VentaDetalleCreate] = Field(min_length=1)


class VentaUpdate(BaseModel):
    cliente_id: int = Field(gt=0)
    detalles: list[VentaDetalleCreate] = Field(min_length=1)


class VentaResponse(BaseModel):
    id: int
    cliente_id: int
    subtotal: float
    iva: float
    total: float
    fecha: datetime
    detalles: list[DetalleVentaResponse] = []
    factura: FacturaResponse | None = None
    model_config = ConfigDict(from_attributes=True)


class MovimientoInventarioCreate(BaseModel):
    producto_id: int = Field(gt=0)
    tipo_movimiento: str = Field(min_length=3, max_length=30)
    cantidad: int = Field(gt=0)
    observacion: str | None = Field(default=None, max_length=255)


class MovimientoInventarioResponse(BaseModel):
    id: int
    producto_id: int
    tipo_movimiento: str
    cantidad: int
    fecha: datetime
    observacion: str | None = None
    model_config = ConfigDict(from_attributes=True)


class CajaCreate(BaseModel):
    saldo_inicial: float = Field(ge=0)


class CajaResponse(BaseModel):
    id: int
    fecha_apertura: datetime
    fecha_cierre: datetime | None = None
    saldo_inicial: float
    saldo_final: float | None = None
    estado: str
    activo: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class MovimientoCajaCreate(BaseModel):
    caja_id: int = Field(gt=0)
    tipo_movimiento: str = Field(min_length=3, max_length=30)
    monto: float = Field(gt=0)
    descripcion: str = Field(min_length=3, max_length=255)


class MovimientoCajaResponse(BaseModel):
    id: int
    caja_id: int
    tipo_movimiento: str
    monto: float
    descripcion: str
    fecha: datetime
    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    username_or_email: str = Field(min_length=3, max_length=150)
    password: str = Field(min_length=8, max_length=128)


class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=10)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class CurrentUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    rol: RolResponse
    activo: bool
    model_config = ConfigDict(from_attributes=True)


class ResumenReportResponse(BaseModel):
    productos: int
    clientes: int
    proveedores: int
    ventas: int
    ingresos: float


class ProductosMasVendidosResponse(BaseModel):
    producto_id: int
    nombre: str
    cantidad_vendida: int
    total_vendido: float


class StockBajoResponse(BaseModel):
    id: int
    nombre: str
    stock: int


class VentasPorMesResponse(BaseModel):
    mes: str
    total_ventas: int
    ingresos: float


class TopClientesResponse(BaseModel):
    cliente_id: int
    nombre: str
    total_compras: int
    total_gastado: float


class InventarioResponse(BaseModel):
    id: int
    nombre: str
    categoria: str
    stock: int
    precio: float
    costo: float
    activo: bool
