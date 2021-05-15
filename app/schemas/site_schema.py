from marshmallow import fields

from app import ma
from app.models import site_model


class SiteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = site_model.SiteModel

    url = fields.URL(required=True)
    hoteis = ma.auto_field()
