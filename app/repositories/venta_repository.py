from app.models.models import Venta


class VentaRepository:
    def listar(self, db):
        return db.query(Venta)

    def obtener_por_id(self, db, venta_id):
        return db.query(Venta).filter(Venta.id == venta_id).first()

    def crear(self, db, venta):
        db.add(venta)
        db.commit()
        db.refresh(venta)
        return venta

    def actualizar(self, db, venta):
        db.commit()
        db.refresh(venta)
        return venta

    def eliminar(self, db, venta):
        venta.activo = False
        db.commit()
        db.refresh(venta)
        return venta