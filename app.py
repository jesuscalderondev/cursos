from flask import Flask, render_template, redirect, jsonify, Blueprint, request
from flask import session as nube
from database import *
from funciones import *

app = Flask("Servidor")


@app.route('/')
def index():
    if validarSesion():
        docente = session.query(Docente).filter(
            Docente.usuario == llaveAcceso()).first()
        if docente != None:
            administrador = session.query(
                Administrador.usuario == llaveAcceso()).first()
            return render_template('administrador.html', administrador=administrador)
        return render_template('docente.html', docente)
    return render_template('index.html')


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
