from datetime import datetime

from app.exceptions import ClienteNoEncontrado
from app.exceptions import StockInsuficiente
from app.exceptions import VentaNoEncontrada
from app.models.models import Caja, Cliente, DetalleVenta, Factura, MovimientoCaja, MovimientoInventario, Producto, Venta
from app.repositories.venta_repository import VentaRepository


repo = VentaRepository()


class VentaService:
    IVA_RATE = 0.15

    def listar(self, db, page=1, size=20, cliente=None, fecha_inicio=None, fecha_fin=None):
        query = db.query(Venta).filter(Venta.activo.is_(True))
        if cliente:
            query = query.join(Cliente).filter(Cliente.nombre.ilike(f"%{cliente}%"))
        if fecha_inicio:
            query = query.filter(Venta.fecha >= datetime.fromisoformat(fecha_inicio))
        if fecha_fin:
            query = query.filter(Venta.fecha <= datetime.fromisoformat(fecha_fin))
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        return {"items": items, "total": total, "page": page, "size": size}

    def obtener_por_id(self, db, venta_id):
        venta = repo.obtener_por_id(db, venta_id)
        if not venta or not venta.activo:
            raise VentaNoEncontrada("Venta no encontrada")
        return venta

    def crear(self, db, payload):
        cliente = db.query(Cliente).filter(Cliente.id == payload.cliente_id, Cliente.activo.is_(True)).first()
        if not cliente:
            raise ClienteNoEncontrado("Cliente no encontrado")

        caja = db.query(Caja).filter(Caja.estado == "ABIERTA", Caja.activo.is_(True)).first()
        if not caja:
            raise ValueError("No existe caja abierta")

        subtotal = 0.0
        detalles = []

        for item in payload.detalles:
            producto = db.query(Producto).filter(Producto.id == item.producto_id, Producto.activo.is_(True)).first()
            if not producto:
                raise ValueError("Producto no encontrado")
            if producto.stock < item.cantidad:
                raise StockInsuficiente("Stock insuficiente")
            producto.stock -= item.cantidad
            detalle_subtotal = producto.precio * item.cantidad
            subtotal += detalle_subtotal
            detalles.append((producto, item.cantidad, detalle_subtotal))

        iva = subtotal * self.IVA_RATE
        total = subtotal + iva

        venta = Venta(cliente_id=payload.cliente_id, subtotal=subtotal, iva=iva, total=total)
        db.add(venta)
        db.flush()

        for producto, cantidad, detalle_subtotal in detalles:
            db.add(DetalleVenta(venta_id=venta.id, producto_id=producto.id, cantidad=cantidad, precio_unitario=producto.precio, subtotal=detalle_subtotal))
            db.add(MovimientoInventario(producto_id=producto.id, tipo_movimiento="SALIDA_VENTA", cantidad=cantidad, observacion=f"Venta #{venta.id}"))

        db.add(Factura(venta_id=venta.id, numero_factura=f"F-{venta.id:08d}", subtotal=subtotal, iva=iva, total=total))
        caja.saldo_final = (caja.saldo_final or caja.saldo_inicial) + total
        db.add(MovimientoCaja(caja_id=caja.id, tipo_movimiento="INGRESO", monto=total, descripcion=f"Venta #{venta.id}"))
        db.commit()
        db.refresh(venta)
        return venta

    def actualizar(self, db, venta_id, payload):
        venta = self.obtener_por_id(db, venta_id)
        venta.cliente_id = payload.cliente_id
        db.commit()
        db.refresh(venta)
        return venta

    def eliminar(self, db, venta_id):
        venta = self.obtener_por_id(db, venta_id)
        return repo.eliminar(db, venta)