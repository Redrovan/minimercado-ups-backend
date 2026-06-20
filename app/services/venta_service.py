from app.models.models import Venta

from app.repositories.venta_repository import VentaRepository

repo = VentaRepository()


class VentaService:

    def listar(self, db):

        return repo.listar(db)

    def crear(self, db, payload):

        venta = Venta(
            cliente_id=payload.cliente_id,
            total=payload.total
        )

        return repo.crear(db, venta)