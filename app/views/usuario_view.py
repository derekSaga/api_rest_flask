from flask import request, make_response, jsonify, render_template
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app import api
from app.decorators_validation import adm_required
from app.entidades import usuario_entidade
from app.schemas import usuario_schema
from app.service import usuario_service


class UsuarioList(Resource):
    # @adm_required
    def post(self):
        us = usuario_schema.UsuarioSchema()
        validate = us.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json['nome']
            email = request.json['email']
            apelido = request.json['apelido']
            senha = request.json['senha']
            dt_nascimento = request.json['dt_nascimento']

            if usuario_service.listar_usuario_apelido(apelido) is not None:
                return make_response(jsonify({'message': 'apelido já está sendo utilizado.'}), 422)

            if usuario_service.listar_usuario_email(email) is not None:
                return make_response(jsonify({'message': 'email já cadastrado.'}), 422)

            usuario_ent = usuario_entidade.UsuarioEntidade(email, apelido, senha, dt_nascimento, nome, is_active=False)

            try:
                result = usuario_service.cadastrar_usuario(usuario_ent)

                s = usuario_service.email_confirmacao(result)
                print(s)
                return make_response(us.jsonify(result), 201)
            except Exception as e:
                usuario_service.delete_usuario(result)
                return make_response(
                    jsonify(
                        {'message': f'{str(e)}'}
                    ),
                    500
                )
                # raise e


class UsuarioDetail(Resource):
    @jwt_required
    def get(self, usuario_id):
        usuario_db = usuario_service.listar_usuario_id(usuario_id)
        if usuario_db is None:
            return make_response(jsonify({'message': 'user not found.'}), 404)
        us = usuario_schema.UsuarioSchema()
        return make_response(us.jsonify(usuario_db), 200)

    @adm_required
    def delete(self, usuario_id):
        usuario_db = usuario_service.listar_usuario_id(usuario_id)
        if usuario_db is None:
            return make_response(jsonify({'message': 'user not found.'}), 404)
        usuario_service.delete_usuario(usuario_db)
        return make_response('', 204)


class UsuarioConfirm(Resource):
    def get(self, usuario_id):
        usuario_db = usuario_service.listar_usuario_id(usuario_id)
        if usuario_db is None:
            return make_response(jsonify({'message': 'user not found.'}), 404)
        else:
            try:
                if usuario_db.is_active:
                    return make_response(jsonify({'message': f'usuario id {usuario_id} cadastro já confirmado.'}), 200)

                usuario_service.ativar_usuario(usuario_db)
                headers = {'Content-Type': 'text/html'}

                return make_response(render_template('confirmacao_usuario.html', usuario=usuario_db.apelido), 200,
                                     headers)

            except Exception as e:
                return make_response(
                    jsonify(
                        {'message': f'{str(e)}'}
                    ),
                    500
                )


api.add_resource(UsuarioList, '/usuario')
api.add_resource(UsuarioDetail, '/usuario/<int:usuario_id>')
api.add_resource(UsuarioConfirm, '/confirma_cadastro/<int:usuario_id>')
