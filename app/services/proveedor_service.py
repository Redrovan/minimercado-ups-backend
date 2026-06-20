from app.exceptions import ProveedorNoEncontrado
from app.models.models import Proveedor
from app.repositories.proveedor_repository import ProveedorRepository


repo = ProveedorRepository()


class ProveedorService:
    def listar(self, db, page=1, size=20, nombre=None, correo=None):
        query = db.query(Proveedor).filter(Proveedor.activo.is_(True))
        if nombre:
            query = query.filter(Proveedor.nombre.ilike(f"%{nombre}%"))
        if correo:
            query = query.filter(Proveedor.correo.ilike(f"%{correo}%"))
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        return {"items": items, "total": total, "page": page, "size": size}

    def obtener_por_id(self, db, proveedor_id):
        proveedor = repo.obtener_por_id(db, proveedor_id)
        if not proveedor or not proveedor.activo:
            raise ProveedorNoEncontrado("Proveedor no encontrado")
        return proveedor

    def crear(self, db, payload):
        proveedor = Proveedor(**payload.model_dump())
        return repo.crear(db, proveedor)

    def actualizar(self, db, proveedor_id, payload):
        proveedor = self.obtener_por_id(db, proveedor_id)
        for field, value in payload.model_dump().items():
            setattr(proveedor, field, value)
        return repo.actualizar(db, proveedor)

    def eliminar(self, db, proveedor_id):
        proveedor = self.obtener_por_id(db, proveedor_id)
        return repo.eliminar(db, proveedor)