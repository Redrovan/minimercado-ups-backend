from app.models.models import Caja
from app.models.models import MovimientoCaja


class CajaService:
    def abrir_caja(self, db, payload):
        if db.query(Caja).filter(Caja.estado == "ABIERTA", Caja.activo.is_(True)).first():
            raise ValueError("Ya existe una caja abierta")
        caja = Caja(saldo_inicial=payload.saldo_inicial, saldo_final=payload.saldo_inicial, estado="ABIERTA")
        db.add(caja)
        db.commit()
        db.refresh(caja)
        return caja

    def cerrar_caja(self, db, caja_id, saldo_final):
        caja = db.query(Caja).filter(Caja.id == caja_id).first()
        if not caja:
            raise ValueError("Caja no encontrada")
        caja.estado = "CERRADA"
        caja.fecha_cierre = __import__("datetime").datetime.utcnow()
        caja.saldo_final = saldo_final
        db.commit()
        db.refresh(caja)
        return caja

    def listar_movimientos(self, db, caja_id):
        return db.query(MovimientoCaja).filter(MovimientoCaja.caja_id == caja_id).all()

    def registrar_movimiento(self, db, payload):
        movimiento = MovimientoCaja(**payload.model_dump())
        db.add(movimiento)
        db.commit()
        db.refresh(movimiento)
        return movimiento
