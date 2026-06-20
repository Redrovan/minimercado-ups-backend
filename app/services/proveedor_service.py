from app.models.models import Proveedor

from app.repositories.proveedor_repository import ProveedorRepository

repo = ProveedorRepository()


class ProveedorService:

    def listar(self, db):

        return repo.listar(db)

    def crear(self, db, payload):

        proveedor = Proveedor(
            ruc=payload.ruc,
            nombre=payload.nombre,
            telefono=payload.telefono,
            correo=payload.correo
        )

        return repo.crear(db, proveedor)