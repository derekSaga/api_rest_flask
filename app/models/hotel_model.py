from app import db


class HotelModel(db.Model):
    __tablename__ = 'hotel'

    hotel_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    estrelas = db.Column(db.Float(precision=1), nullable=False)
    diaria = db.Column(db.Float(precision=2), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    site_id = db.Column(db.Integer,
                        db.ForeignKey('site.site_id'),
                        nullable=False)
