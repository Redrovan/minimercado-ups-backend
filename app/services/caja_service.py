from datetime import datetime

from app.exceptions import CajaAbiertaError, CajaCerradaError, CajaNoEncontrada
from app.models.models import Caja, MovimientoCaja


class CajaService:
    def abrir_caja(self, db, payload):
        caja_abierta = db.query(Caja).filter(
            Caja.estado == "ABIERTA", Caja.activo.is_(True)
        ).first()
        if caja_abierta:
            raise CajaAbiertaError("Ya existe una caja abierta")
        caja = Caja(
            saldo_inicial=payload.saldo_inicial,
            saldo_final=payload.saldo_inicial,
            estado="ABIERTA",
        )
        db.add(caja)
        db.commit()
        db.refresh(caja)
        return caja

    def cerrar_caja(self, db, caja_id, saldo_final):
        caja = db.query(Caja).filter(Caja.id == caja_id, Caja.activo.is_(True)).first()
        if not caja:
            raise CajaNoEncontrada("Caja no encontrada")
        if caja.estado == "CERRADA":
            raise CajaCerradaError("La caja ya está cerrada")
        caja.estado = "CERRADA"
        caja.fecha_cierre = datetime.utcnow()
        caja.saldo_final = saldo_final
        db.commit()
        db.refresh(caja)
        return caja

    def obtener_caja_abierta(self, db):
        caja = db.query(Caja).filter(
            Caja.estado == "ABIERTA", Caja.activo.is_(True)
        ).first()
        if not caja:
            raise CajaNoEncontrada("No hay ninguna caja abierta")
        return caja

    def listar_movimientos(self, db, caja_id):
        caja = db.query(Caja).filter(Caja.id == caja_id, Caja.activo.is_(True)).first()
        if not caja:
            raise CajaNoEncontrada("Caja no encontrada")
        return db.query(MovimientoCaja).filter(MovimientoCaja.caja_id == caja_id).all()

    def registrar_movimiento(self, db, payload):
        caja = db.query(Caja).filter(
            Caja.id == payload.caja_id, Caja.activo.is_(True)
        ).first()
        if not caja:
            raise CajaNoEncontrada("Caja no encontrada")
        if caja.estado == "CERRADA":
            raise CajaCerradaError("No se pueden registrar movimientos en una caja cerrada")
        movimiento = MovimientoCaja(**payload.model_dump())
        db.add(movimiento)
        db.commit()
        db.refresh(movimiento)
        return movimiento