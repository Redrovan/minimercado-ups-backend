from app.exceptions import ClienteNoEncontrado
from app.models.models import Cliente
from app.repositories.cliente_repository import ClienteRepository


repo = ClienteRepository()


class ClienteService:
    def listar(self, db, page=1, size=20, nombre=None, correo=None):
        query = db.query(Cliente).filter(Cliente.activo.is_(True))
        if nombre:
            query = query.filter(Cliente.nombre.ilike(f"%{nombre}%"))
        if correo:
            query = query.filter(Cliente.correo.ilike(f"%{correo}%"))
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        return {"items": items, "total": total, "page": page, "size": size}

    def obtener_por_id(self, db, cliente_id):
        cliente = repo.obtener_por_id(db, cliente_id)
        if not cliente or not cliente.activo:
            raise ClienteNoEncontrado("Cliente no encontrado")
        return cliente

    def crear(self, db, payload):
        cliente = Cliente(**payload.model_dump())
        return repo.crear(db, cliente)

    def actualizar(self, db, cliente_id, payload):
        cliente = self.obtener_por_id(db, cliente_id)
        for field, value in payload.model_dump().items():
            setattr(cliente, field, value)
        return repo.actualizar(db, cliente)

    def eliminar(self, db, cliente_id):
        cliente = self.obtener_por_id(db, cliente_id)
        return repo.eliminar(db, cliente)