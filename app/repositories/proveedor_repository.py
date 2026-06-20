from app.models.models import Proveedor


class ProveedorRepository:

    def listar(self, db):

        return db.query(Proveedor).all()

    def crear(self, db, proveedor):

        db.add(proveedor)

        db.commit()

        db.refresh(proveedor)

        return proveedor