from flask import Flask, render_template, redirect, jsonify, Blueprint, request
from flask import session as nube
from database import *
from funciones import *

app = Flask("Servidor")

@app.route('/')
def index():
    if validarSesion():
        docente = session.query(Docente).filter(Docente.usuario == llaveAcceso()).first()
        if docente != None:
            administrador = session.query(Administrador.usuario == llaveAcceso()).first()
            return render_template('administrador.html', administrador = administrador)
        return render_template('docente.html', docente)
    return render_template('index.html')

@app.route('/inicio_sesion', methods = ['POST'])
def iniciarSesion():
    operacion = "Fallida"
    if validarSesion() != True:
        credenciales = request.get_json()
        clave = credenciales["clave"]
        email = credenciales["email"]
        if verificar_caracteres_especiales(nombre_usuario) == True and verificar_caracteres_especiales(clave) == True:
            usuario = session.query(Usuario).filter(
                Usuario.email == email).first()
            
            if usuario != None and validarClave(usuario.clave, clave):
                nube['llave_ingreso'] = usuario.ID
                operacion = "Exitosa"
            else:
                mensaje = 'Usuario o clave incorrect@'
        else:
            mensaje = "Caracteres especiales detectados, por favor intentar sin insertar caracteres como '@,/.#'"
            
    return jsonify(respuesta = operacion, mensaje = mensaje)



        

#------------------------------------  Cursos ------------------------------------
cursos = Blueprint("cursos", __name__, url_prefix='/cursos')

@cursos.route('/lista')
def listarCursos():
    respuesta = redirect('/')
    if validarSesion():
        respuesta = render_template('cursos.html')
    return respuesta

#----------------------------------- Docentes ------------------------------------
docentes = Blueprint("docentes", __name__, url_prefix='/docentes')

@docentes.route('/lista')
def listarDocentes():
    respuesta = redirect('/')
    if validarSesion():
        respuesta = render_template('docentes.html')
    return respuesta

#--------------------------------- API'S -------------------------------------
apis = Blueprint("apis", __name__, url_prefix='/api')

@apis.route('/filtrar_docente', methods = ['POST', 'GET'])
def filtrarDocente():
    if request.method == 'GET':
        respuesta = jsonify(respuesta = "Acceso denegado")
    if validarSesion() and request.method == 'POST':
        peticion = request.get_json()
        campo = peticion['filtrado']
        consulta = session.query(Docente).filter(or_(Docente.nombres.like(f'%{campo}%'), Docente.apellido_paterno).like(f'%{campo}%'), Docente.apellido_materno.like(f'%{campo}%')).all()
        
        json_docentes = {'respuesta' : 'Acceso concedido', 'docentes' : {}}
        for docente in consulta:
            json_docentes[f'{docente.id}'] = {
                'nombres' : docente.nombre,
                'paterno' : docente.apellido_paterno,
                'materno' : docente.apellido_materno,
                'email' : docente.email,
                'id' : docente.id
            }
        
        respuesta = json_docentes
    return respuesta

app.register_blueprint(apis)

if __name__ == '__main__':
    app.run(debug=True)