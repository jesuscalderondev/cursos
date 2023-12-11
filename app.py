from flask import Flask, render_template, redirect, jsonify, Blueprint, request
from flask import session as nube
from database import *
from funciones import *
from cargadorEstudiantes2 import Cargador

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
        if session.query(AsistenciaDocente).filter(AsistenciaDocente.fecha == datetime.now().date(), AsistenciaDocente.docente == docente.id).first() == None:
            asistencia = AsistenciaDocente(docente.id)
            session.add(asistencia)
            session.commit()
        grupos = session.query(Grupo).filter(Grupo.docente == docente.id, and_(Grupo.fecha_inicial <= datetime.now().date(), Grupo.fecha_final >= datetime.now().date())).all()
        return renderizarLista('docente.html', grupos, None)
    return render_template('index.html')

@app.route('/cerrar_sesion')
def cerrarSesion():
    if validarSesion():
        nube.pop('llave_ingreso')
    return redirect("/")

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
        try:
            crearAdministrador(formulario)
            return "Exitosamente creado el administrador"
        except:
            return "Error, el correo electronico ya se encuentra en uso"
    else:
        return render_template("registrarAdministrador.html")


@app.route('/migrar', methods = ['POST', 'GET'])
def subirEstudiantes():
    respuesta = "Sin acceso a esta acción"
    if validarSesion():
        if request.method == 'POST':
            archivo = request.files["archivo"]
            print(archivo)
            if ".xlsx" in archivo.filename or ".xls" in archivo.filename:
                
                Cargador(archivo)
                respuesta = "Los datos fueron cargados exitosamente a la base de datos "
                """ except:
                    respuesta = "Error, verifique que los datos cumplan con los estandares y no hayan campos vacíos" """
            else:
                respuesta = "El archivo no es un excel por favor verifique que el archivo sea correcto"  
            return jsonify(mensaje = respuesta)
        return renderizarTemplate("migrar.html")
    return respuesta

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
        return renderizarLista("listarCursos.html", lista,  None)
    return redirect("/")

@cursos.route('/editar/<int:id>')
def editarCursoFormulario(id):
    if validarSesion():
        curso = session.get(Curso, id)
        return renderizarEditCurso("editarCurso.html", curso)
    return redirect("/")

@cursos.route('/ver/<int:id>')
def listarGruposDeUnCurso(id):
    if validarSesion():
        grupos = session.query(Grupo).filter(Grupo.curso == id).all()
        json = []
        for i in grupos:
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
        return renderizarLista("listarGrupos.html", json, None)
    return redirect("/")

@cursos.route('/eliminar/<int:id>')
def eliminarCurso(id):
    if validarSesion():
        curso = session.get(Curso, id)
        session.delete(curso)
        session.commit()
        return redirect("/curso/lista")
    return redirect("/")

@cursos.route('/actualizar', methods=["POST"])
def editarCurso():
    operacion = "Fallida"
    mensaje = "Sin modificaciones"
    if validarSesion():
        formulario = request.get_json()
        actualizarCurso(formulario)
        operacion = "Exitosa"
        mensaje = "Curso actualizado exitosamanete"
    return jsonify(respuesta = operacion, mensaje = mensaje)

app.register_blueprint(cursos)
#----------------------------------- Docentes ------------------------------------
docentes = Blueprint("docentes", __name__, url_prefix='/docente')

@docentes.route('/lista')
def listarDocentes():
    respuesta = redirect('/')
    if validarSesion():
        lista = session.query(Docente).all()
        lista2 = []
        
        for i in lista:
            lista2.append(session.get(Usuario, i.usuario).email)
        respuesta = renderizarListas('listarDocentes.html', lista, lista2)
    return respuesta

@docentes.route('/crear', methods=['POST', 'GET'])
def regsitrarDocente():
    if validarSesion():
        if request.method == 'POST':
            formulario = request.get_json()
            try:
                print("SIIIU")
                clave = crearDocente(formulario)
                operacion = "Exitosa"
                mensaje = "Docente registrado de manera exitosa"
            except:
                operacion = "Fallida"
                mensaje = "Correo electronico usado con anterioridad"
                clave = "sin clave"
            return jsonify(respuesta = operacion, mensaje = mensaje, clave = clave)
        else:
            rol = session.get(Usuario, llaveAcceso())
            return renderizarTemplate("crearDocente.html")
    return redirect('/')

@docentes.route('/editar/<int:id>')
def editarDocenteFormulario(id):
    if validarSesion():
        docente = session.get(Docente, id)
        return renderizarEditDocente("editarDocente.html", docente)
    return redirect("/")

@docentes.route('/actualizar', methods = ['POST'])
def editarDocente():
    operacion = "Fallida"
    mensaje = "Sin modificaciones"
    if validarSesion():
        formulario = request.get_json()
        actualizarDocente(formulario)
        operacion = "Exitosa"
        mensaje = "Docente actualizado exitosamanete"
    return jsonify(respuesta = operacion, mensaje = mensaje)

@docentes.route('/mis_grupos')
def listarMisGrupos():
    if validarSesion() and session.get(Usuario, llaveAcceso()).rol == "Docente":
        docente = session.query(Docente).filter(Docente.usuario == llaveAcceso()).first()
        grupos = session.query(Grupo).filter(Grupo.docente == docente.id).all()
        json = []
        docente = f'{docente.nombres} {docente.apellido_paterno}'
        for i in grupos:
            curso = session.get(Curso, i.curso)
            json.append({
                'docente' : docente,
                'curso' : curso.nombre,
                'nombre' : i.nombre,
                'horario' : f'{i.hora_inicial} a {i.hora_final}',
                'dias' : i.dias_de_clases[:-2],
                'codigo' : i.codigo
            })
        return renderizarLista("listarGrupos.html", json, None)
    return redirect("/")

app.register_blueprint(docentes)

#--------------------------------- API'S -------------------------------------
apis = Blueprint("apis", __name__, url_prefix='/api')

@apis.route('/filtrar_docente', methods = ['POST', 'GET'])
def filtrarDocente():
    respuesta = "Sin accceso"
    if validarSesion() and request.method == 'POST':
        peticion = request.get_json()
        campo = peticion['filtrado']
        if campo != "":
            consulta = session.query(Docente).filter(or_(Docente.nombres.like(f'%{campo}%'), Docente.apellido_paterno.like(f'%{campo}%'), Docente.apellido_materno.like(f'%{campo}%'))).all()
        else:
            consulta = session.query(Docente).all()
        json_docentes = {}
        
        for docente in consulta:
            json_docentes[f'{docente.id}'] = {
                'nombres' : docente.nombres,
                'paterno' : docente.apellido_paterno,
                'materno' : docente.apellido_materno,
                'email' : session.get(Usuario, docente.usuario).email,
                'id' : docente.id
            }
        
        respuesta = json_docentes
    return jsonify(respuesta = "Exitosa", json = json_docentes)

@apis.route('/filtrar_curso', methods = ['POST'])
def filtrarCurso():
    if validarSesion():
        formulario = request.get_json()
        parametro = formulario["filtro"]
        
        cursos_filtrados = session.query(Curso).filter(or_(Curso.nombre.like(f'%{parametro}%'), Curso.duracion.like(f'%{parametro}%'), Curso.ciclo.like(f'%{parametro}%'))).all()
        
        json_cursos = {}
        
        for i in cursos_filtrados:
            json_cursos[f'{i.codigo}'] = {
                'nombre' : i.nombre,
                'ciclo' : i.ciclo,
                'duracion' : i.duracion,
                'codigo' : i.codigo
            }
        
        respuesta = json_cursos
    return jsonify(respuesta = "Exitosa", json=json_cursos)

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

@apis.route('/obtener_registros_cursos')
def enviarDatosEstudiantes():
    if validarSesion():
        alumnos = session.query(Estudiante).all()
        
        json = {'cursos' : [], 'estudiantes' : [], 'totalEstudiantes' : len(alumnos), 'totalDocentes' : obtenerCantidad(Docente), 'totalCursos' : obtenerCantidad(Curso), 'totalGrupos' : obtenerCantidad(Grupo)}
        for i in alumnos:
            grupo = session.get(Grupo, i.grupo)
            curso = session.get(Curso, grupo.curso)
            if curso.nombre in json['cursos']:
                json['estudiantes'][json['cursos'].index(curso.nombre)] += 1
            else:
                json['cursos'].append(curso.nombre)
                json['estudiantes'].append(1)
    print(json)
    return jsonify(datos = json, respuesta = "Exitosa")

@apis.route('/obtener_promedio_asistencias')
def enviarDatosDocente():
    if validarSesion():
        
        meses_lista = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        docente = session.query(Docente).filter(Docente.usuario == llaveAcceso()).first()
        grupos = session.query(Grupo).filter(Grupo.docente == docente.id).all()
        json = {'grupos' : [], 'promedios' : [], 'meses' : [], 'mis_asistencias': []}
        print(grupos)
        for i in grupos:
            asistencias = session.query(AsistenciaEstudiante).filter(AsistenciaEstudiante.grupo == i.codigo, AsistenciaEstudiante.asiste == True, and_(AsistenciaEstudiante.fecha >= i.fecha_inicial, AsistenciaEstudiante.fecha <= i.fecha_final)).all()
            suma = 0
            meses = []
            for asistencia in asistencias:
                suma += 1
                if asistencia.fecha.month not in meses:
                    meses.append(asistencia.fecha.month)
            json["grupos"].append(i.nombre)
            try:
                prom = round(suma/len(meses))
            except:
                prom = 0
            json['promedios'].append(prom)
        for i in meses_lista:
            mes = meses_lista.index(i)+1
            if mes < 10:
                mes = f'0{mes}'
            print(f"%{datetime.now().date().year}-{mes}%")
            mis_asistencias = session.query(AsistenciaDocente).filter(and_(AsistenciaDocente.fecha.like(f"%{datetime.now().date().year}-{mes}%"))).all()
            if i not in json["meses"]:
                json["meses"].append(i)
                json["mis_asistencias"].append(len(mis_asistencias))
            
    print(json)
    return jsonify(datos = json, respuesta = "Exitosa")

@apis.route('/firmar_asistencia/docente/<int:id>/<int:grupo>')
def firmarAsistenciaDocente(id, grupo):
    if validarSesion():
        asistencia = AsistenciaDocente(id, datetime.now().date(), grupo)
        session.add(asistencia)
        session.commit()
    return redirect('/')

@apis.route('/firmar_asistencia/estudiante/<int:id>/<int:grupo>')
def firmarAsistenciaEstudiante(id, grupo):
    if validarSesion():
        asistencia = AsistenciaEstudiante(id, datetime.now().date(), grupo)
        session.add(asistencia)
        session.commit()
    return redirect('/')

@apis.route('/confirmar_asistencia/<int:codigo>')
def confirmarAsistencia(codigo):
    if validarSesion():
        try:
            estudiante = session.get(Estudiante, codigo)
            asistencia = AsistenciaEstudiante(codigo, estudiante.grupo, True)
            session.add(asistencia)
            session.commit()
            return redirect(f"/grupo/{estudiante.grupo}/asistencia")
        except:
            return "Error este estudioante ya tiene asistencia"
    return redirect("/")

@apis.route('/confirmar_inasistencia/<int:codigo>')
def confirmarInasistencia(codigo):
    if validarSesion():
        try:
            estudiante = session.get(Estudiante, codigo)
            asistencia = AsistenciaEstudiante(codigo, estudiante.grupo, False)
            session.add(asistencia)
            session.commit()
            return redirect(f"/grupo/{estudiante.grupo}/asistencia")
        except:
            return "Error este estudioante ya tiene asistencia"
    return redirect("/")

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

@grupos.route('/actualizar', methods=['GET', 'POST'])
def editarGrupo():
    if validarSesion():
        if request.method == "POST":

            formulario = request.get_json()
            actualizarGrupo(formulario)
            mensaje = "Grupo Actualizado exitosamente"
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
        return renderizarLista("listarGrupos.html", json, None)
    return redirect("/")

@grupos.route('/eliminar/<string:codigo>', methods = ['GET'])
def eliminarGrupo(codigo):
    mensaje = "Sin acceso"
    if validarSesion():
        try:
            grupo = session.get(Grupo, codigo)
            session.delete(grupo)
            session.commit()
            return redirect('/grupo/lista')
        except:
            return "Este registro no existe"
    return jsonify(mensaje = mensaje)

@grupos.route('/editar/<string:codigo>', methods = ['GET'])
def editarGrupoFormulario(codigo):
    respuesta = redirect("/")
    if validarSesion():
        try:
            grupo = session.get(Grupo, codigo)
            return renderizarEditGrupo("editarGrupo.html", grupo)
        except:
            mensaje = "El grupo no existe"
    return jsonify(mensaje = mensaje)

        
@grupos.route('/ver/<string:codigo>')
def listarEstudiantesDeUnGrupo(codigo):
    if validarSesion():
        estudiantes = session.query(Estudiante).filter(Estudiante.grupo == codigo).all()
        json = []
        grupo = session.get(Grupo, codigo)
        curso = session.get(Curso, grupo.curso)
        for i in estudiantes:
            json.append({
                'grupo' : grupo.nombre,
                'curso' : curso.nombre,
                'nombre' : i.nombre,
                'codigo' : i.codigo,
                'diaDePago' : i.dia_de_pago
            })
    return renderizarLista("listarEstudiantes.html", json, grupo)

@grupos.route('/<string:codigo>/asistencia')
def asistenciaFormulario(codigo):
    if validarSesion():
        estudiantes = session.query(Estudiante).filter(Estudiante.grupo == codigo).all()
        json = []
        grupo = session.get(Grupo, codigo)
        curso = session.get(Curso, grupo.curso)
        for i in estudiantes:
            if session.query(AsistenciaEstudiante).filter(AsistenciaEstudiante.fecha == datetime.now().date(), AsistenciaEstudiante.estudiante == i.codigo, AsistenciaEstudiante.grupo == codigo).first() == None:
                json.append({
                    'grupo' : grupo.nombre,
                    'curso' : curso.nombre,
                    'nombre' : i.nombre,
                    'codigo' : i.codigo,
                    'diaDePago' : i.dia_de_pago
                })
    return renderizarLista("asistencia.html", json, grupo)

app.register_blueprint(grupos)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)