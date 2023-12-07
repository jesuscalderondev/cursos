from flask import Flask, render_template, redirect, jsonify, Blueprint, request
from flask import session as nube
from database import *
from funciones import *

app = Flask("Servidor")
app.config["SECRET_KEY"] = "KJSDKLDSJBNCDSBS"

@app.route('/')
def index():
    if validarSesion():
        docente = session.query(Docente).filter(Docente.usuario == llaveAcceso()).first()
        if docente == None:
            administrador = session.query(Administrador).filter(Administrador.usuario == llaveAcceso()).first()
            if administrador != None:
                rol = session.get(Usuario, administrador.usuario)
                return render_template('administrador.html', usuario = administrador, rol = rol)
            rol = session.get(Usuario, docente.usuario)
        return render_template('docente.html', usuario = docente, rol = rol)
    return render_template('index.html')

@app.route('/inicio_sesion', methods = ['POST'])
def iniciarSesion():
    operacion = "Fallida"
    mensaje = "Sin mensaje"
    if validarSesion() != True:
        credenciales = request.get_json()
        print(credenciales)
        
        clave = credenciales["clave"]
        email = credenciales["email"]
        usuario = session.query(Usuario).filter(
            Usuario.email == email).first()
        
        print(validarClave(usuario.clave, clave))
        
        if usuario != None and validarClave(usuario.clave, clave):
            nube['llave_ingreso'] = usuario.id
            operacion = "Exitosa"
        else:
            mensaje = 'Usuario o clave incorrect@'
            
    return jsonify(respuesta = operacion, mensaje = mensaje)



@app.route('/registrar_dministrador', methods = ['POST', 'GET'])
def registrarAdministrador():
    print(request.method)
    if request.method == 'POST':
        formulario = request.form
        print(formulario)
        crearAdministrador(formulario)
        return "Exitosamente creado el administrador"
    else:
        return render_template("registrarAdministrador.html")

@app.route('/registrar_docente', methods=['POST', 'GET'])
def regsitrarDocente():
    if validarSesion():
        if request.method == 'POST':
            formulario = request.get_json()
            try:
                print("SIIIU")
                crearDocente(formulario)
                operacion = "Exitosa"
                mensaje = "Docente registrado de manera exitosa"
            except:
                operacion = "Fallida"
                mensaje = "Correo electronico usado con anterioridad"
            return jsonify(respuesta = operacion, mensaje = mensaje)
        else:
            rol = session.get(Usuario, llaveAcceso())
            return render_template("crearDocente.html", rol = rol, usuario = obtenerRol(rol))
    return redirect('/')

""" 
@app.route('/subir_estudiantes', methods = ['POST'])
def subirEstudiantes():
    if validarSesion():
        archivo = request.files["archivo"]
        
        if ".xlsx" in archivo.filename:
            archivo.save("/static/listaEstudiantes.xlsx")

    return  """
        

#------------------------------------  Cursos ------------------------------------
cursos = Blueprint("cursos", __name__, url_prefix='/cursos')

@cursos.route('/lista')
def listarCursos():
    respuesta = redirect('/')
    if validarSesion():
        respuesta = render_template('cursos.html')
    return respuesta

@cursos.route('/crear', methods=['GET', 'POST'])
def registrarCurso():
    if validarSesion():
        if request.method == 'POST':
            formulario = request.get_json()
            try:
                crearCurso(formulario)
                operacion = "Exitosa"
                mensaje = "Curso creado de manera satisfactoria"
            except:
                operacion = "Fallida"
                mensaje = "El curso no fue creado, debido a que este curso ya existe"
            return jsonify(respuesta = operacion, mensaje = mensaje)
        else:
            return render_template("crearCurso.html")
            
    return redirect("/")

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
    Base.metadata.create_all(engine)
    app.run(debug=True)