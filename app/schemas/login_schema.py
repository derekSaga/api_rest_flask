from marshmallow import fields

from app import ma


class LoginSchema(ma.Schema):
    apelido = fields.String(required=True)
    senha = fields.String(required=True)
