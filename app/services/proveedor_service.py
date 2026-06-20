from fastapi import HTTPException

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

        proveedor = repo.obtener_por_id(
            db,
            proveedor_id
        )

        if not proveedor:

            raise HTTPException(
                status_code=404,
                detail="Proveedor no encontrado"
            )

        return proveedor

    def crear(
        self,
        db,
        payload
    ):

        if len(payload.ruc) != 13:

            raise HTTPException(
                status_code=400,
                detail="El RUC debe tener 13 dígitos"
            )

        if "@" not in payload.correo:

            raise HTTPException(
                status_code=400,
                detail="Correo inválido"
            )

        if len(payload.telefono) < 10:

            raise HTTPException(
                status_code=400,
                detail="Teléfono inválido"
            )

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

            raise HTTPException(
                status_code=404,
                detail="Proveedor no encontrado"
            )

        if len(payload.ruc) != 13:

            raise HTTPException(
                status_code=400,
                detail="El RUC debe tener 13 dígitos"
            )

        if "@" not in payload.correo:

            raise HTTPException(
                status_code=400,
                detail="Correo inválido"
            )

        if len(payload.telefono) < 10:

            raise HTTPException(
                status_code=400,
                detail="Teléfono inválido"
            )

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

            raise HTTPException(
                status_code=404,
                detail="Proveedor no encontrado"
            )

        repo.eliminar(
            db,
            proveedor
        )

        return {
            "mensaje": "Proveedor eliminado correctamente"
        }