from fastapi import HTTPException

from app.models.models import Venta

from app.repositories.venta_repository import (
    VentaRepository
)

repo = VentaRepository()


class VentaService:

    def listar(self, db):

        return repo.listar(db)

    def obtener_por_id(
        self,
        db,
        venta_id
    ):

        return repo.obtener_por_id(
            db,
            venta_id
        )

    def crear(
        self,
        db,
        payload
    ):

        if payload.total <= 0:

            raise HTTPException(
                status_code=400,
                detail="El total debe ser mayor a cero"
            )

        venta = Venta(
            cliente_id=payload.cliente_id,
            total=payload.total
        )

        return repo.crear(
            db,
            venta
        )

    def actualizar(
        self,
        db,
        venta_id,
        payload
    ):

        venta = repo.obtener_por_id(
            db,
            venta_id
        )

        if not venta:

            raise HTTPException(
                status_code=404,
                detail="Venta no encontrada"
            )

        if payload.total <= 0:

            raise HTTPException(
                status_code=400,
                detail="El total debe ser mayor a cero"
            )

        venta.cliente_id = payload.cliente_id
        venta.total = payload.total

        return repo.actualizar(
            db,
            venta
        )

    def eliminar(
        self,
        db,
        venta_id
    ):

        venta = repo.obtener_por_id(
            db,
            venta_id
        )

        if not venta:

            raise HTTPException(
                status_code=404,
                detail="Venta no encontrada"
            )

        repo.eliminar(
            db,
            venta
        )

        return {
            "mensaje": "Venta eliminada"
        }