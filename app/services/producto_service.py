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
    
def obtener_por_id(self, db, producto_id):

    return repo.obtener_por_id(db, producto_id)


def eliminar(self, db, producto_id):

    producto = repo.obtener_por_id(
        db,
        producto_id
    )

    if not producto:
        return None

    repo.eliminar(
        db,
        producto
    )

    return {
        "mensaje": "Producto eliminado"
    }

def actualizar(
    self,
    db,
    producto_id,
    payload
):

    producto = repo.obtener_por_id(
        db,
        producto_id
    )

    if not producto:
        return None

    producto.codigo_barras = payload.codigo_barras
    producto.nombre = payload.nombre
    producto.categoria = payload.categoria
    producto.costo = payload.costo
    producto.precio = payload.precio
    producto.stock = payload.stock

    return repo.actualizar(
        db,
        producto
    )