from app.exceptions import ProductoNoEncontrado
from app.models.models import Producto
from app.repositories.producto_repository import ProductoRepository


repo = ProductoRepository()


class ProductoService:
    def listar(self, db, page=1, size=20, nombre=None, categoria=None, stock_minimo=None):
        query = db.query(Producto).filter(Producto.activo.is_(True))
        if nombre:
            query = query.filter(Producto.nombre.ilike(f"%{nombre}%"))
        if categoria:
            query = query.filter(Producto.categoria.ilike(f"%{categoria}%"))
        if stock_minimo is not None:
            query = query.filter(Producto.stock >= stock_minimo)
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        return {"items": items, "total": total, "page": page, "size": size}

    def obtener_por_id(self, db, producto_id):
        producto = repo.obtener_por_id(db, producto_id)
        if not producto or not producto.activo:
            raise ProductoNoEncontrado("Producto no encontrado")
        return producto

    def crear(self, db, payload):
        producto = Producto(**payload.model_dump())
        return repo.crear(db, producto)

    def actualizar(self, db, producto_id, payload):
        producto = self.obtener_por_id(db, producto_id)
        for field, value in payload.model_dump().items():
            setattr(producto, field, value)
        return repo.actualizar(db, producto)

    def eliminar(self, db, producto_id):
        producto = self.obtener_por_id(db, producto_id)
        return repo.eliminar(db, producto)