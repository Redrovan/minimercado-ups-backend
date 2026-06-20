from app.models.models import Producto


class ProductoRepository:

    def listar(self, db):

        return db.query(Producto).all()

    def crear(self, db, producto):

        db.add(producto)
        db.commit()
        db.refresh(producto)

        return producto