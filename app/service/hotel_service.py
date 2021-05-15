from app import db
from app.models import hotel_model


def listar_hoteis():
    hoteis = hotel_model.HotelModel.query.all()
    return hoteis


def listar_hotel_id(id_hotel, args=None):
    hotel = hotel_model.HotelModel.query.filter(hotel_model.HotelModel.hotel_id == id_hotel).first()
    return hotel


def editar_hotel(hotel_db, hotel_entidade):
    hotel_db.nome = hotel_entidade.nome
    hotel_db.estrelas = hotel_entidade.estrelas
    hotel_db.diaria = hotel_entidade.diaria
    hotel_db.cidade = hotel_entidade.cidade
    hotel_db.estado = hotel_entidade.estado
    hotel_db.site_id = hotel_entidade.site_id
    try:
        db.session.commit()
        return hotel_db
    except Exception as e:
        db.session.rollback()
        raise e


def delete_hotel(hotel_db):
    try:
        db.session.delete(hotel_db)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def cadastrar_hotel(hotel_entidade):
    hotel_db = hotel_model.HotelModel(
        nome=hotel_entidade.nome,
        estrelas=hotel_entidade.estrelas,
        diaria=hotel_entidade.diaria,
        cidade=hotel_entidade.cidade,
        estado=hotel_entidade.estado,
        site_id=hotel_entidade.site_id
    )
    try:
        db.session.add(hotel_db)
        db.session.commit()
        return hotel_db
    except Exception as e:
        db.session.rollback()
        raise e
