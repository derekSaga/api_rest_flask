from app.models import site_model
from flask import make_response, request, jsonify
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource

from app import pagination, api
from app.entidades import site_entidade
from app.models import hotel_model
from app.schemas import site_schema
from app.service import site_service


class SiteList(Resource):
    def get(self):
        hs = site_schema.SiteSchema(many=True)
        return make_response(
            pagination.paginate(site_model.SiteModel, hs), 200
        )

    @jwt_required
    def post(self):
        hs = site_schema.SiteSchema()
        validate = hs.validate(request.json)
        if validate:
            return make_response(
                jsonify(validate),
                400
            )
        else:
            url = request.json['url']
            site_db = site_service.listar_site(url)
            if site_db:
                return make_response(
                    jsonify({'message': 'the site is already registered'}
                            ),
                    422
                )
            else:
                site_ent = site_entidade.SiteEntidade(url)
                try:
                    site_db = site_service.cadastrar_site(site_ent)
                    return make_response(hs.jsonify(site_db), 200)
                except Exception as e:
                    msg = 'Um erro interno ocorreu ao tentar salvar o Hotel'
                    return make_response(
                        jsonify(
                            {
                                'message': msg,
                                'error': f'{e}'
                            }
                        ),
                        500)


class SiteDetail(Resource):
    def get(self, site_id):
        ss = site_schema.SiteSchema()
        try:
            site_db = site_service.listar_site_id(site_id)
            if site_db is None:
                return make_response(jsonify("Site não encontrado"), 404)
            else:
                return make_response(ss.jsonify(site_db), 200)
        except Exception as e:
            msg = f'Um erro ocorreu ao tentar listar o hotel com id  {site_id}'
            return make_response(
                jsonify(
                    {
                        'message': msg,
                        'error': f'{e}'
                    }
                ),
                500
            )

    def delete(self, site_id):
        try:
            site_db = site_service.listar_site_id(site_id)
            if site_db is None:
                return make_response(jsonify("Site não encontrado"), 404)
            site_service.delete_site(site_db)
            return make_response('', 204)
        except Exception as e:
            msg = 'Um erro ocorreu ao tentar deletar o site'
            return make_response(
                jsonify(
                    {
                        'message': msg,
                        'error': f'{e}'
                    }
                ),
                500
            )

    def put(self,  site_id):
        ss = site_schema.SiteSchema()
        validate = ss.validate(request.json)

        if validate:
            return make_response(jsonify(validate), 400)
        else:
            site_db = site_service.listar_site_id(site_id)
            site_entity = site_entidade.SiteEntidade(**request.json)
            try:
                result = site_service.update_site(site_db, site_entity)
                return make_response(ss.jsonify(result), 200)
            except Exception as e:
                msg = 'Um erro interno ocorreu ao tentar atualizar o Site'
                return make_response(
                    jsonify(
                        {
                            'message': msg,
                            'error': f'{e}'
                        }
                    ),
                    500)


api.add_resource(SiteList, '/site')
api.add_resource(SiteDetail, '/site/<int:site_id>')
