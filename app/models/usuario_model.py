from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app import db


class UsuarioModel(db.Model):
    __tablename__ = 'usuario'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    apelido = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(150), nullable=False)
    dt_nascimento = db.Column(db.Date, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)

    def gen_senha(self):
        self.senha = pbkdf2_sha256.hash(self.senha)

    def ver_senha(self, senha):
        return pbkdf2_sha256.verify(senha, self.senha)
