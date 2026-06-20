from app.exceptions import AppException
from app.models.models import Rol
from app.repositories.rol_repository import RolRepository


repo = RolRepository()


class RolService:
    def listar(self, db):
        return repo.listar(db)

    def obtener_por_id(self, db, rol_id):
        rol = repo.obtener_por_id(db, rol_id)
        if not rol:
            raise AppException("Rol no encontrado")
        return rol

    def crear(self, db, payload):
        if repo.obtener_por_nombre(db, payload.nombre):
            raise AppException("El rol ya existe")
        rol = Rol(nombre=payload.nombre, descripcion=payload.descripcion)
        return repo.crear(db, rol)

    def actualizar(self, db, rol_id, payload):
        rol = self.obtener_por_id(db, rol_id)
        rol.nombre = payload.nombre
        rol.descripcion = payload.descripcion
        return repo.actualizar(db, rol)

    def eliminar(self, db, rol_id):
        rol = self.obtener_por_id(db, rol_id)
        rol.activo = False
        return repo.actualizar(db, rol)
