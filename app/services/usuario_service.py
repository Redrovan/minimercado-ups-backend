from app.exceptions import AppException
from app.exceptions import UsuarioNoEncontrado
from app.models.models import Usuario
from app.repositories.rol_repository import RolRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.security import hash_password


repo = UsuarioRepository()
rol_repo = RolRepository()


class UsuarioService:
    def listar(self, db):
        return db.query(Usuario).all()

    def obtener_por_id(self, db, usuario_id):
        usuario = repo.obtener_por_id(db, usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado("Usuario no encontrado")
        return usuario

    def crear(self, db, payload):
        if not rol_repo.obtener_por_id(db, payload.rol_id):
            raise AppException("Rol no encontrado")
        usuario = Usuario(
            username=payload.username,
            email=payload.email,
            password_hash=hash_password(payload.password),
            rol_id=payload.rol_id,
            activo=payload.activo,
        )
        return repo.crear(db, usuario)

    def actualizar(self, db, usuario_id, payload):
        usuario = self.obtener_por_id(db, usuario_id)
        usuario.username = payload.username
        usuario.email = payload.email
        usuario.rol_id = payload.rol_id
        usuario.activo = payload.activo
        if payload.password:
            usuario.password_hash = hash_password(payload.password)
        return repo.actualizar(db, usuario)

    def eliminar(self, db, usuario_id):
        usuario = self.obtener_por_id(db, usuario_id)
        usuario.activo = False
        return repo.actualizar(db, usuario)
