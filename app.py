from flask import Flask, render_template, redirect, jsonify, Blueprint, request
from flask import session as nube
from database import *
from funciones import *

app = Flask("Servidor")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/docentes/listar')
def docentesListar():
    return render_template('listarDocentes.html')


@app.route('/docente/crear')
def docenteCrear():
    return render_template('crearDocente.html')


@app.route('/estudiantes/listar')
def estudiantesCrear():
    return render_template('listarEstudiantes.html')


@app.route('/cursos/listar')
def cursosCrear():
    return render_template('listarCursos.html')


@app.route('/curso/crear')
def cursoCrear():
    return render_template('crearCurso.html')


@app.route('/grupos/listar')
def gruposCrear():
    return render_template('listarGrupos.html')


@app.route('/grupo/crear')
def grupoCrear():
    return render_template('crearGrupo.html')


# Cursos
cursos = Blueprint("cursos", __name__, url_prefix='/cursos')


@cursos.route('/lista')
def listarCursos():
    respuesta = redirect('/')
    if validarSesion():
        respuesta = render_template('cursos.html')
    return respuesta


if __name__ == '__main__':
    app.run(debug=True)
