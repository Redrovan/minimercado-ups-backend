from app.models.models import Usuario


class UsuarioRepository:
    def listar(self, db):
        return db.query(Usuario).all()

    def obtener_por_id(self, db, usuario_id):
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def obtener_por_username_o_email(self, db, username_or_email):
        return (
            db.query(Usuario)
            .filter((Usuario.username == username_or_email) | (Usuario.email == username_or_email))
            .first()
        )

    def crear(self, db, usuario):
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    def actualizar(self, db, usuario):
        db.commit()
        db.refresh(usuario)
        return usuario
