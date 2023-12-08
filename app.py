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
                return renderizarTemplate('administrador.html')
            rol = session.get(Usuario, docente.usuario)
        return renderizarTemplate('docente.html')
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



@app.route('/registrar_administrador', methods = ['POST', 'GET'])
def registrarAdministrador():
    print(request.method)
    if request.method == 'POST':
        formulario = request.form
        print(formulario)
        crearAdministrador(formulario)
        return "Exitosamente creado el administrador"
    else:
        return render_template("registrarAdministrador.html")


""" 
@app.route('/subir_estudiantes', methods = ['POST'])
def subirEstudiantes():
    if validarSesion():
        archivo = request.files["archivo"]
        
        if ".xlsx" in archivo.filename:
            archivo.save("/static/listaEstudiantes.xlsx")

    return  """
        

#------------------------------------  Cursos ------------------------------------
cursos = Blueprint("cursos", __name__, url_prefix='/curso')


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
            return renderizarTemplate("crearCurso.html")
            
    return redirect("/")

@cursos.route('/lista')
def listarCursos():
    if validarSesion():
        lista = session.query(Curso).all()
        print(lista)
        return renderizarLista("listarCursos.html", lista)
    return redirect("/")

app.register_blueprint(cursos)
#----------------------------------- Docentes ------------------------------------
docentes = Blueprint("docentes", __name__, url_prefix='/docente')

@docentes.route('/lista')
def listarDocentes():
    respuesta = redirect('/')
    if validarSesion():
        lista = session.query(Docente).all()
        respuesta = renderizarLista('listarDocentes.html', lista)
    return respuesta

@docentes.route('/crear', methods=['POST', 'GET'])
def regsitrarDocente():
    if validarSesion():
        print(request.method)
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
            return renderizarTemplate("crearDocente.html")
    return redirect('/')

app.register_blueprint(docentes)

#--------------------------------- API'S -------------------------------------
apis = Blueprint("apis", __name__, url_prefix='/api')

@apis.route('/filtrar_docente', methods = ['POST', 'GET'])
def filtrarDocente():
    respuesta = "Sin accceso"
    if validarSesion() and request.method == 'POST':
        peticion = request.get_json()
        campo = peticion['filtrado']
        consulta = session.query(Docente).filter(or_(Docente.nombres.like(f'%{campo}%'), Docente.apellido_paterno).like(f'%{campo}%'), Docente.apellido_materno.like(f'%{campo}%')).all()
        
        json_docentes = {}
        
        for docente in consulta:
            json_docentes[f'{docente.id}'] = {
                'nombres' : docente.nombres,
                'paterno' : docente.apellido_paterno,
                'materno' : docente.apellido_materno,
                'email' : docente.email,
                'id' : docente.id
            }
        
        respuesta = json_docentes
    return respuesta

@apis.route('/filtrar_curso')
def filtrarCurso():
    if validarSesion():
        formulario = request.get_json()
        parametro = formulario["filtro"]
        
        cursos_filtrados = session.query(Curso).filter(or_(Curso.nombre.like(f'%{parametro}%'), Curso.duracion.like(f'%{parametro}%'), Curso.ciclo.like(f'%{parametro}%'))).all()
        
        json_cursos = {}
        
        for i in cursos_filtrados:
            json_cursos[f'{i.id}'] = {
                'nombre' : i.nombre,
                'ciclo' : i.ciclo,
                'duracion' : i.duracion
            }
        
        respuesta = json_cursos
    return respuesta

@apis.route('/filtrar_grupo', methods=['POST'])
def filtrarGrupo():
    if validarSesion():
        formulario = request.get_json()
        parametro = formulario["filtro"]
        
        grupos_filtrados = session.query(Grupo).filter(or_(Grupo.codigo.like(f'%{parametro}%'), Grupo.nombre.like(f'%{parametro}%'), Grupo.hora_inicial.like(f'%{parametro}%'), Grupo.hora_final.like(f'%{parametro}%'), Grupo.hora_inicial.like(f'%{parametro}%'), Grupo.dias_de_clases.like(f'%{parametro}%'))).all()
        
        json = {}
        
        for i in grupos_filtrados:
            if i.docente != None:
                docente = session.get(Docente, i.docente)
                docente = f'{docente.nombres} {docente.apellido_paterno}'
            else:
                docente = "Sin asignar"
            curso = session.get(Curso, i.curso)
            
            json[f'{i.codigo}'] = {
                'docente' : docente,
                'curso' : curso.nombre,
                'nombre' : i.nombre,
                'horario' : f'{i.hora_inicial} a {i.hora_final}',
                'dias' : i.dias_de_clases[:-2],
                'codigo' : i.codigo
            }
        return jsonify(respuesta = "Exitosa", json = json)
    return jsonify(respuesta = "Fallida")
app.register_blueprint(apis)


#-------------------------------------- Grupos -----------------------------------------
grupos = Blueprint("grupos", __name__, url_prefix="/grupo")

@grupos.route('/crear', methods=['GET', 'POST'])
def registrarGrupo():
    if validarSesion():
        if request.method == "POST":

            formulario = request.get_json()
            crearGrupo(formulario)
            mensaje = "Grupo creado exitosamente"
            operacion = "Exitosa"
        
            return jsonify(mensaje = mensaje, respuesta = operacion)
        rol = session.get(Usuario, llaveAcceso())
        listaDocentes = session.query(Docente).all()
        listaCursos = session.query(Curso).all()
        return render_template("crearGrupo.html", rol = rol, usuario = obtenerRol(rol), docentes = listaDocentes, cursos = listaCursos)
    return redirect('/')

@grupos.route('/lista')
def listarGrupos():
    if validarSesion():
        lista = session.query(Grupo).all()
        json = []
        
        for i in lista:
            if i.docente != None:
                docente = session.get(Docente, i.docente)
                docente = f'{docente.nombres} {docente.apellido_paterno}'
            else:
                docente = "Sin asignar"
            curso = session.get(Curso, i.curso)
            print(i.codigo)
            json.append({
                'docente' : docente,
                'curso' : curso.nombre,
                'nombre' : i.nombre,
                'horario' : f'{i.hora_inicial} a {i.hora_final}',
                'dias' : i.dias_de_clases[:-2],
                'codigo' : i.codigo
            })
        return renderizarLista("listarGrupos.html", lista = json)
    return redirect("/")

@grupos.route('/eliminar/<string:codigo>', methods = ['GET'])
def eliminarGrupo(codigo):
    mensaje = "Sin acceso"
    if validarSesion():
        try:
            grupo = session.get(Grupo, codigo)
            session.delete(grupo)
            session.commit()
            mensaje = "El grupo fue eliminado"
        except:
            mensaje = "El grupo no existe"
    return jsonify(mensaje = mensaje)

@grupos.route('/editar/<string:codigo>', methods = ['GET'])
def editarGrupo(codigo):
    respuesta = redirect("/")
    if validarSesion():
        try:
            grupo = session.get(Grupo, codigo)
            renderizarEdit("editarGrupo", registro = grupo)
        except:
            mensaje = "El grupo no existe"
    return jsonify(mensaje = mensaje)


app.register_blueprint(grupos)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)