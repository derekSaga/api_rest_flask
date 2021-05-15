from marshmallow import fields

from app import ma
from app.models import hotel_model


class HotelSchema(ma.SQLAlchemySchema):
    class Meta:
        model = hotel_model.HotelModel
        # fields = ('hotel_id', 'nome', 'estrelas', 'diaria', 'cidade', 'estado')

    hotel_id = fields.Integer()
    nome = fields.String(required=True)
    estrelas = fields.Float(required=True)
    diaria = fields.Float(required=True)
    cidade = fields.String(required=True)
    estado = fields.String(required=True)
    site_id = fields.Integer(required=True, load_only=True)
