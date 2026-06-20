from app.models.models import Cliente

from app.repositories.cliente_repository import ClienteRepository

repo = ClienteRepository()


class ClienteService:

    def listar(self, db):

        return repo.listar(db)

    def crear(self, db, payload):

        cliente = Cliente(
            cedula=payload.cedula,
            nombre=payload.nombre,
            telefono=payload.telefono,
            correo=payload.correo
        )

        return repo.crear(db, cliente)