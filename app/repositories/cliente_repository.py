from app.models.models import Cliente


class ClienteRepository:

    def listar(self, db):

        return db.query(Cliente).all()

    def crear(self, db, cliente):

        db.add(cliente)

        db.commit()

        db.refresh(cliente)

        return cliente