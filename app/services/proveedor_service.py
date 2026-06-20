from app.models.models import Proveedor

from app.repositories.proveedor_repository import (
    ProveedorRepository
)

repo = ProveedorRepository()


class ProveedorService:

    def listar(self, db):

        return repo.listar(db)

    def obtener_por_id(
        self,
        db,
        proveedor_id
    ):

        return repo.obtener_por_id(
            db,
            proveedor_id
        )

    def crear(
        self,
        db,
        payload
    ):

        proveedor = Proveedor(
            ruc=payload.ruc,
            nombre=payload.nombre,
            telefono=payload.telefono,
            correo=payload.correo
        )

        return repo.crear(
            db,
            proveedor
        )

    def actualizar(
        self,
        db,
        proveedor_id,
        payload
    ):

        proveedor = repo.obtener_por_id(
            db,
            proveedor_id
        )

        if not proveedor:
            return None

        proveedor.ruc = payload.ruc
        proveedor.nombre = payload.nombre
        proveedor.telefono = payload.telefono
        proveedor.correo = payload.correo

        return repo.actualizar(
            db,
            proveedor
        )

    def eliminar(
        self,
        db,
        proveedor_id
    ):

        proveedor = repo.obtener_por_id(
            db,
            proveedor_id
        )

        if not proveedor:
            return None

        repo.eliminar(
            db,
            proveedor
        )

        return {
            "mensaje": "Proveedor eliminado"
        }