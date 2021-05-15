from flask import url_for, request
from requests import post

from app import db
from app.constants import MAILGUN_DOMAIN, YOUR_API_KEY, FROM_EMAIL, FROM_TITLE
from app.entidades.usuario_entidade import UsuarioEntidade
from app.models import usuario_model
from app.models.usuario_model import UsuarioModel


def cadastrar_usuario(usuario_ent: UsuarioEntidade):
    usuario_db = usuario_model.UsuarioModel(nome=usuario_ent.nome,
                                            email=usuario_ent.email,
                                            apelido=usuario_ent.apelido,
                                            senha=usuario_ent.senha,
                                            dt_nascimento=usuario_ent.dt_nascimento,
                                            is_active=usuario_ent.is_active)
    try:
        usuario_db.gen_senha()
        db.session.add(usuario_db)
        db.session.commit()
        return usuario_db
    except Exception as e:
        return {'message': f'{str(e)}'}
        # raise e


def listar_usuario_id(usuario_id):
    usuario_db = UsuarioModel.query.filter(UsuarioModel.id_usuario == usuario_id).first()
    return usuario_db


def listar_usuario_apelido(apelido):
    usuario_db = UsuarioModel.query.filter(UsuarioModel.apelido == apelido).first()
    return usuario_db


def listar_usuario_email(email):
    usuario_db = UsuarioModel.query.filter(UsuarioModel.email == email).first()
    return usuario_db


def ativar_usuario(usuario_db):
    usuario_db.is_active = True
    db.session.commit()


def delete_usuario(usuario_db):
    try:
        db.session.delete(usuario_db)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {'message': f'{e}'}


def email_confirmacao(usuario_db):
    url_root = request.url_root[:-1] + url_for('usuarioconfirm', usuario_id=usuario_db.id_usuario)
    data = {
        "from": f"NO-REPLY <{FROM_EMAIL}>",
        "to": [usuario_db.email],
        "subject": f"{FROM_TITLE}",
        "text": "Teste de Validação de email",
        "html": '<html><p>Confirme seu cadastro clicando no link a seguir:'
                ' <a href="{}">CONFIRMAR EMAIL</a> </p> </html>'.format(url_root)
    }
    return post(
        "https://api.mailgun.net/v3/{}/messages".format(MAILGUN_DOMAIN),
        auth=('api', YOUR_API_KEY),
        data=data
    )
