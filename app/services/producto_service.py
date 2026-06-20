from fastapi import HTTPException

from app.models.models import Producto
from app.repositories.producto_repository import ProductoRepository

repo = ProductoRepository()


class ProductoService:

    def listar(self, db):

        return repo.listar(db)

    def obtener_por_id(
        self,
        db,
        producto_id
    ):

        producto = repo.obtener_por_id(
            db,
            producto_id
        )

        if not producto:

            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        return producto

    def crear(
        self,
        db,
        payload
    ):

        if payload.precio <= 0:

            raise HTTPException(
                status_code=400,
                detail="El precio debe ser mayor a cero"
            )

        if payload.costo < 0:

            raise HTTPException(
                status_code=400,
                detail="Costo inválido"
            )

        if payload.stock < 0:

            raise HTTPException(
                status_code=400,
                detail="El stock no puede ser negativo"
            )

        producto = Producto(
            codigo_barras=payload.codigo_barras,
            nombre=payload.nombre,
            categoria=payload.categoria,
            costo=payload.costo,
            precio=payload.precio,
            stock=payload.stock
        )

        return repo.crear(
            db,
            producto
        )

    def actualizar(
        self,
        db,
        producto_id,
        payload
    ):

        producto = repo.obtener_por_id(
            db,
            producto_id
        )

        if not producto:

            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        if payload.precio <= 0:

            raise HTTPException(
                status_code=400,
                detail="El precio debe ser mayor a cero"
            )

        if payload.costo < 0:

            raise HTTPException(
                status_code=400,
                detail="Costo inválido"
            )

        if payload.stock < 0:

            raise HTTPException(
                status_code=400,
                detail="El stock no puede ser negativo"
            )

        producto.codigo_barras = payload.codigo_barras
        producto.nombre = payload.nombre
        producto.categoria = payload.categoria
        producto.costo = payload.costo
        producto.precio = payload.precio
        producto.stock = payload.stock

        return repo.actualizar(
            db,
            producto
        )

    def eliminar(
        self,
        db,
        producto_id
    ):

        producto = repo.obtener_por_id(
            db,
            producto_id
        )

        if not producto:

            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        repo.eliminar(
            db,
            producto
        )

        return {
            "mensaje": "Producto eliminado correctamente"
        }