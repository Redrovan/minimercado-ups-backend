from app.models.models import Cliente


class ClienteRepository:

    def listar(self, db):

        return db.query(Cliente).all()

    def crear(self, db, cliente):

        db.add(cliente)

        db.commit()

        db.refresh(cliente)

        return cliente
    
    from app.models.models import Cliente


class ClienteRepository:

    def listar(self, db):
        return db.query(Cliente).all()

    def obtener_por_id(self, db, cliente_id):

        return (
            db.query(Cliente)
            .filter(
                Cliente.id == cliente_id
            )
            .first()
        )

    def crear(self, db, cliente):

        db.add(cliente)

        db.commit()

        db.refresh(cliente)

        return cliente

    def actualizar(self, db, cliente):

        db.commit()

        db.refresh(cliente)

        return cliente

    def eliminar(self, db, cliente):

        db.delete(cliente)

        db.commit()