from app import db
from app.models import site_model


def cadastrar_site(site_ent):
    site_db = site_model.SiteModel(url=site_ent.url)
    db.session.add(site_db)
    db.session.commit()
    return site_db


def listar_site(url):
    site_db = site_model.SiteModel.query.filter(
        site_model.SiteModel.url == url
    ).first()
    return site_db


def listar_site_id(site_id):
    site_db = site_model.SiteModel.query.filter(
        site_model.SiteModel.site_id == site_id
    ).first()
    return site_db


def delete_site(site_db):
    db.session.delete(site_db)
    db.session.commit()


def update_site(site_db, site_entidade):
    site_db.url = site_entidade.url
    db.session.commit()
    return site_db
