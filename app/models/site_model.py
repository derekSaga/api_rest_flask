from app import db


class SiteModel(db.Model):
    __tablename__ = 'site'

    site_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(150), nullable=False, unique=True)
    hoteis = db.relationship('HotelModel', cascade="all, delete")
