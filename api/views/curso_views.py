from flask_restful import Resource
from api import api
from ..schermas import curso_schema
from flask import request, make_response, jsonify
from ..entidades import curso
from ..services import curso_services

class CursoList(Resource):
    def get(self):
        #chamndo a função listar
        cursos = curso_services.listar_curso()
        #validando com schema e trazendo tdos os registro
        cs = curso_schema.CursoSchema(many=True)
        #retornando um make_resp onde deve ser o formato JSON
        return make_response(cs.jsonify(cursos), 200)

    def post(self):
        cs = curso_schema.CursoSchema()
        validate = cs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            data_publicacao = request.json["data_publicacao"]

            novo_curso = curso.Curso(nome=nome, descricao=descricao, data_publicacao=data_publicacao)
            resultado = curso_services.cadastrar_curso(novo_curso)
            x = cs.jsonify(resultado)
            return make_response(x, 201)

class CursoDetail(Resource):
    def get(self, id):
        curso = curso_services.listar_curso_id(id)
        if curso is None:
            return make_response(jsonify("Curso não foi encontrado"), 404)
        cs = curso_schema.CursoSchema()
        return make_response(cs.jsonify(curso), 200)

    def put(self, id):
        curso_bd = curso_services.listar_curso_id(id)
        if curso_bd is None:
            return make_response(jsonify("curso não foi encontrado"), 404)
        cs = curso_schema.CursoSchema()
        validate = cs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 404)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            data_publicacao = request.json["data_publicacao"]
            novo_curso = curso.Curso(nome=nome, descricao=descricao, data_publicacao=data_publicacao)

            #atualizar
            curso_services.atualiza_cursos(curso_bd, novo_curso)
            curso_atualizado = curso_services.listar_curso_id(id)
            return make_response(cs.jsonify(curso_atualizado), 200)

    def delete(self, id):
        curso_db = curso_services.listar_curso_id(id)
        if curso_db is None:
            return make_response(jsonify("Curso não achado"), 404)
        curso_services.remove_curso(curso_db)
        return make_response("Excluido com sucesso", 200)


api.add_resource(CursoList, '/cursos')
api.add_resource(CursoDetail, '/cursos/<int:id>')