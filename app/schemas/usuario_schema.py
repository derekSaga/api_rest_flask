from marshmallow import fields

from app import ma
from app.models import usuario_model


class UsuarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = usuario_model.UsuarioModel
    id_usuario = fields.Integer(required=False, load_only=False)
    nome = fields.Str(required=True)
    email = fields.Str(required=True)
    apelido = fields.Str(required=True)
    dt_nascimento = fields.Date(required=True)
    senha = fields.Str(required=True, load_only=True)
    is_active = fields.Boolean(required=False, dump_only=True)
