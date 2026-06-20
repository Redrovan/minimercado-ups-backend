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
    
def obtener_por_id(
    self,
    db,
    cliente_id
):

    return repo.obtener_por_id(
        db,
        cliente_id
    )


def actualizar(
    self,
    db,
    cliente_id,
    payload
):

    cliente = repo.obtener_por_id(
        db,
        cliente_id
    )

    if not cliente:
        return None

    cliente.cedula = payload.cedula
    cliente.nombre = payload.nombre
    cliente.telefono = payload.telefono
    cliente.correo = payload.correo

    return repo.actualizar(
        db,
        cliente
    )


def eliminar(
    self,
    db,
    cliente_id
):

    cliente = repo.obtener_por_id(
        db,
        cliente_id
    )

    if not cliente:
        return None

    repo.eliminar(
        db,
        cliente
    )

    return {
        "mensaje": "Cliente eliminado"
    }