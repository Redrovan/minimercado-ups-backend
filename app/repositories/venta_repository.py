from app.models.models import Venta


class VentaRepository:

    def listar(self, db):

        return db.query(Venta).all()

    def crear(self, db, venta):

        db.add(venta)

        db.commit()

        db.refresh(venta)

        return venta