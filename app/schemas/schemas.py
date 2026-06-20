from pydantic import BaseModel


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