from app.models.models import Proveedor


class ProveedorRepository:

    def listar(self, db):

        return db.query(Proveedor).all()

    def obtener_por_id(
        self,
        db,
        proveedor_id
    ):

        return (
            db.query(Proveedor)
            .filter(
                Proveedor.id == proveedor_id
            )
            .first()
        )

    def crear(
        self,
        db,
        proveedor
    ):

        db.add(proveedor)

        db.commit()

        db.refresh(proveedor)

        return proveedor

    def actualizar(
        self,
        db,
        proveedor
    ):

        db.commit()

        db.refresh(proveedor)

        return proveedor

    def eliminar(
        self,
        db,
        proveedor
    ):

        db.delete(proveedor)

        db.commit()