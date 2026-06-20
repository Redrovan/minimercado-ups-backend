from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from datetime import datetime

from app.database import Base


class Producto(Base):

    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    codigo_barras = Column(String, unique=True)
    nombre = Column(String)
    categoria = Column(String)
    costo = Column(Float)
    precio = Column(Float)
    stock = Column(Integer)


class Cliente(Base):

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True)
    nombre = Column(String)
    telefono = Column(String)
    correo = Column(String)


class Proveedor(Base):

    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    ruc = Column(String, unique=True)
    nombre = Column(String)
    telefono = Column(String)
    correo = Column(String)

class Venta(Base):

    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)

    cliente_id = Column(Integer)

    total = Column(Float)

    fecha = Column(
        DateTime,
        default=datetime.utcnow
    )