from app.exceptions import ProveedorNoEncontrado
from app.models.models import Producto, Proveedor
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
        result = [self._serializar(prov) for prov in items]
        return {"items": result, "total": total, "page": page, "size": size}

    def _serializar(self, proveedor):
        return {
            "id": proveedor.id,
            "ruc": proveedor.ruc,
            "nombre": proveedor.nombre,
            "telefono": proveedor.telefono,
            "correo": proveedor.correo,
            "activo": proveedor.activo,
            "created_at": proveedor.created_at,
            "updated_at": proveedor.updated_at,
            "producto_ids": [p.id for p in proveedor.productos],
        }

    def _obtener(self, db, proveedor_id):
        """Retorna el objeto ORM, usado internamente."""
        proveedor = repo.obtener_por_id(db, proveedor_id)
        if not proveedor or not proveedor.activo:
            raise ProveedorNoEncontrado("Proveedor no encontrado")
        return proveedor

    def obtener_por_id(self, db, proveedor_id):
        """Retorna dict serializado, usado por la API."""
        return self._serializar(self._obtener(db, proveedor_id))

    def _sync_productos(self, db, proveedor, producto_ids):
        """Sincroniza los productos asociados al proveedor."""
        if not producto_ids:
            proveedor.productos = []
        else:
            productos = db.query(Producto).filter(Producto.id.in_(producto_ids), Producto.activo.is_(True)).all()
            proveedor.productos = productos
        db.commit()
        db.refresh(proveedor)

    def crear(self, db, payload):
        data = payload.model_dump(exclude={"producto_ids"})
        producto_ids = payload.producto_ids or []
        proveedor = Proveedor(**data)
        repo.crear(db, proveedor)
        if producto_ids:
            self._sync_productos(db, proveedor, producto_ids)
        return self._serializar(proveedor)

    def actualizar(self, db, proveedor_id, payload):
        proveedor = self._obtener(db, proveedor_id)
        data = payload.model_dump(exclude={"producto_ids"})
        for field, value in data.items():
            setattr(proveedor, field, value)
        repo.actualizar(db, proveedor)
        self._sync_productos(db, proveedor, payload.producto_ids or [])
        return self._serializar(proveedor)

    def asignar_productos(self, db, proveedor_id, producto_ids):
        """Asigna productos a un proveedor existente."""
        proveedor = self._obtener(db, proveedor_id)
        self._sync_productos(db, proveedor, producto_ids)
        return self._serializar(proveedor)

    def eliminar(self, db, proveedor_id):
        proveedor = self._obtener(db, proveedor_id)
        return repo.eliminar(db, proveedor)
