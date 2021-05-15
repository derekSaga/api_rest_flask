import datetime

from flask import request, make_response, jsonify
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from app import api, jwt
from app.schemas import login_schema
from app.service import usuario_service


class LoginList(Resource):
    @jwt.user_claims_loader
    def add_claim_to_access_token(identify):
        usuario_db = usuario_service.listar_usuario_email(identify)
        if usuario_db.is_admin:
            roles = 'admin'
        else:
            roles = 'user'
        return {'roles': roles}

    def post(self):
        ls = login_schema.LoginSchema()
        validate = ls.validate(request.json)

        if validate:
            return make_response(jsonify({'message': validate}), 401)
        else:
            apelido = request.json['apelido']
            senha = request.json['senha']

            usuario_db = usuario_service.listar_usuario_apelido(
                apelido=apelido)

            user_validate = usuario_db is None or usuario_db.is_active is False or not usuario_db.ver_senha(
                senha=senha)

            if user_validate:
                return make_response(jsonify({'message': 'usuario não entrado ou não está ativo.'}), 403)

            token_access = create_access_token(identity=usuario_db.email,
                                               expires_delta=datetime.timedelta(seconds=60))

            return make_response(jsonify({'message': 'login efetuado com sucesso',
                                          'token_access': token_access}), 200)


api.add_resource(LoginList, '/login')
