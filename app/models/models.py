from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.database import Base


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SoftDeleteMixin:
    activo = Column(Boolean, default=True, nullable=False, index=True)


class Rol(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(80), unique=True, nullable=False, index=True)
    descripcion = Column(String(255), nullable=True)

    usuarios = relationship("Usuario", back_populates="rol")


class Usuario(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    rol = relationship("Rol", back_populates="usuarios")


class Producto(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    codigo_barras = Column(String(80), unique=True, nullable=False, index=True)
    nombre = Column(String(150), nullable=False, index=True)
    categoria = Column(String(120), nullable=False, index=True)
    costo = Column(Float, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)

    detalles_venta = relationship("DetalleVenta", back_populates="producto")
    movimientos_inventario = relationship("MovimientoInventario", back_populates="producto")


class Cliente(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(150), nullable=False, index=True)
    telefono = Column(String(20), nullable=False)
    correo = Column(String(150), unique=True, nullable=False, index=True)

    ventas = relationship("Venta", back_populates="cliente")


class Proveedor(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    ruc = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(150), nullable=False, index=True)
    telefono = Column(String(20), nullable=False)
    correo = Column(String(150), nullable=False)


class Venta(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    subtotal = Column(Float, nullable=False, default=0)
    iva = Column(Float, nullable=False, default=0)
    total = Column(Float, nullable=False, default=0)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

    cliente = relationship("Cliente", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")
    factura = relationship("Factura", back_populates="venta", uselist=False, cascade="all, delete-orphan")


class DetalleVenta(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "detalles_venta"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_venta")


class Factura(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), unique=True, nullable=False)
    numero_factura = Column(String(50), unique=True, nullable=False, index=True)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    subtotal = Column(Float, nullable=False)
    iva = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    venta = relationship("Venta", back_populates="factura")


class MovimientoInventario(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "movimientos_inventario"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    tipo_movimiento = Column(String(30), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    observacion = Column(String(255), nullable=True)

    producto = relationship("Producto", back_populates="movimientos_inventario")


class Caja(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "cajas"

    id = Column(Integer, primary_key=True, index=True)
    fecha_apertura = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_cierre = Column(DateTime, nullable=True)
    saldo_inicial = Column(Float, nullable=False, default=0)
    saldo_final = Column(Float, nullable=True)
    estado = Column(String(20), nullable=False, default="ABIERTA")

    movimientos = relationship("MovimientoCaja", back_populates="caja", cascade="all, delete-orphan")


class MovimientoCaja(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "movimientos_caja"

    id = Column(Integer, primary_key=True, index=True)
    caja_id = Column(Integer, ForeignKey("cajas.id"), nullable=False)
    tipo_movimiento = Column(String(30), nullable=False)
    monto = Column(Float, nullable=False)
    descripcion = Column(String(255), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

    caja = relationship("Caja", back_populates="movimientos")