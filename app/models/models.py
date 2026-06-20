from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

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