from app.models.models import Rol


class RolRepository:
    def listar(self, db):
        return db.query(Rol).all()

    def obtener_por_id(self, db, rol_id):
        return db.query(Rol).filter(Rol.id == rol_id).first()

    def obtener_por_nombre(self, db, nombre):
        return db.query(Rol).filter(Rol.nombre == nombre).first()

    def crear(self, db, rol):
        db.add(rol)
        db.commit()
        db.refresh(rol)
        return rol

    def actualizar(self, db, rol):
        db.commit()
        db.refresh(rol)
        return rol
