from app.models.models import Producto
from app.repositories.producto_repository import ProductoRepository

repo = ProductoRepository()


class ProductoService:

    def listar(self, db):

        return repo.listar(db)

    def crear(self, db, payload):

        producto = Producto(
            codigo_barras=payload.codigo_barras,
            nombre=payload.nombre,
            categoria=payload.categoria,
            costo=payload.costo,
            precio=payload.precio,
            stock=payload.stock
        )

        return repo.crear(db, producto)