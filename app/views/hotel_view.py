from flask import make_response, jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from app import api
from app.decorators_validation import adm_required
from app.entidades.hotel_entidade import HotelEntidade
from app.models.hotel_model import HotelModel
from app.pagination import paginate
from app.schemas import hotel_schema
from app.schemas.hotel_schema import HotelSchema
from app.service import hotel_service


def filter_args(params):
    args_parsed = params.parse_args()
    if args_parsed['cidade'] is None:
        del args_parsed['cidade']
        filter_spec = [
            {
                'field': 'estrelas',
                'op': '>=',
                'value': args_parsed['estrelas_min']
            },
            {
                'field': 'estrelas', 'op': '<=',
                'value': args_parsed['estrelas_max']
            },
            {
                'field': 'diaria',
                'op': '>=',
                'value': args_parsed['diaria_min']
            },
            {
                'field': 'diaria',
                'op': '<=',
                'value': args_parsed['diaria_max']
            }
        ]

    else:
        filter_spec = [
            {
                'field': 'cidade',
                'op': '==',
                'value': args_parsed['cidade']
            },

            {
                'field': 'estrelas',
                'op': '>=',
                'value': args_parsed['estrelas_min']
            },
            {
                'field': 'estrelas',
                'op': '<=',
                'value': args_parsed['estrelas_max']
            },
            {
                'field': 'diaria',
                'op': '>=',
                'value': args_parsed['diaria_min']
            },
            {
                'field': 'diaria',
                'op': '<=',
                'value': args_parsed['diaria_max']
            }
        ]
    return filter_spec


path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float, default=1)
path_params.add_argument('estrelas_max', type=float, default=5)
path_params.add_argument('diaria_min', type=float, default=0)
path_params.add_argument('diaria_max', type=float, default=120000)


class HotelList(Resource):
    @jwt_required
    def get(self):
        hs = hotel_schema.HotelSchema(many=True)
        filter_hotel = filter_args(path_params)
        try:
            return make_response(paginate(HotelModel, hs, filter_hotel), 200)
        except Exception as e:
            return make_response(
                jsonify({'message': 'internal error server',
                         'error': f'{e}'}),
                500)

    @adm_required
    def post(self):
        hs = HotelSchema()
        validate = hs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:

            nome = request.json['nome']
            estrelas = request.json['estrelas']
            diaria = request.json['diaria']
            cidade = request.json['cidade']
            estado = request.json['estado']
            site_id = request.json['site_id']
            hotel_novo = HotelEntidade(
                nome, estrelas, diaria, cidade, estado, site_id)
            try:
                hotel_db = hotel_service.cadastrar_hotel(hotel_novo)
                return make_response(hs.jsonify(hotel_db), 201)
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


class HotelDetail(Resource):
    @jwt_required
    def get(self, hotel_id):

        hotel_db = hotel_service.listar_hotel_id(hotel_id)
        if hotel_db is None:
            return make_response(jsonify("Hotel não encontrado"), 404)
        hs = HotelSchema()
        return make_response(hs.jsonify(hotel_db), 200)

    @jwt_required
    def put(self, hotel_id):
        hotel_db = hotel_service.listar_hotel_id(hotel_id)

        if hotel_db is None:
            return make_response(jsonify("Hotel não encontrado"), 404)
        hs = HotelSchema()

        validate = hs.validate(request.json)

        if validate:
            return make_response(jsonify(validate), 400)
        else:

            nome = request.json['nome']
            estrelas = request.json['estrelas']
            diaria = request.json['diaria']
            cidade = request.json['cidade']
            estado = request.json['estado']
            site_id = request.json['site_id']

            hotel_novo = HotelEntidade(
                nome, estrelas, diaria, cidade, estado, site_id)

            try:
                hotel_result = hotel_service.editar_hotel(hotel_db, hotel_novo)
                return make_response(hs.jsonify(hotel_result), 200)
            except Exception as e:
                msg = 'Um erro ocorreu ao tentar atualizar o hotel'
                return make_response(
                    jsonify(
                        {
                            'message': msg,
                            'error': f'{e}'
                        }
                    ),
                    500
                )

    @adm_required
    def delete(self, hotel_id):
        hotel_db = hotel_service.listar_hotel_id(hotel_id)
        if hotel_db is None:
            return make_response(jsonify("Hotel não encontrado"), 404)
        try:
            hotel_service.delete_hotel(hotel_db)
            return make_response('', 204)
        except Exception as e:
            return make_response(
                jsonify(
                    {
                        'message': 'Um erro ocorreu ao tentar deleta o hotel',
                        'error': f'{e}'
                    }
                ),
                500
            )


api.add_resource(HotelList, '/hoteis')
api.add_resource(HotelDetail, '/hoteis/<int:hotel_id>')
