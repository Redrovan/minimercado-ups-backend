from app.models.models import Producto


class ProductoRepository:
    def listar(self, db):
        return db.query(Producto)

    def obtener_por_id(self, db, producto_id):
        return db.query(Producto).filter(Producto.id == producto_id).first()

    def crear(self, db, producto):
        db.add(producto)
        db.commit()
        db.refresh(producto)
        return producto

    def actualizar(self, db, producto):
        db.commit()
        db.refresh(producto)
        return producto

    def eliminar(self, db, producto):
        producto.activo = False
        db.commit()
        db.refresh(producto)
        return producto