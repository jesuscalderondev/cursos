from flask import session as nube
from flask import render_template
import hashlib
import base64
from database import *
from random import randint
import bcrypt

def validarSesion():
    if "llave_ingreso" in nube:
        return True
    return False

def codificar(clave):
    sal = bcrypt.gensalt()
    hash_clave = bcrypt.hashpw(clave.encode(), sal)
    return hash_clave


def validarClave(clave_codificada, clave_decodificada):
    try:
        bcrypt.checkpw(clave_decodificada.encode(), clave_codificada)
        return True
    except:
        return False


def verificar_caracteres_especiales(texto):
    texto = str(texto)
    for caracter in texto:
        if not caracter.isalnum():
            return False
    return True

def generarClave(nombre, apellido):
    clave = nombre.split(" ")[0] + apellido + f'{randint(0, 127)}'
    clave = clave.lower()
    return clave

def llaveAcceso():
    return nube["llave_ingreso"]


def crearDocente(form):
    nombres = form['nombres']
    apellidoPaterno = form['apellidoPaterno']
    apellidoMaterno = form['apellidoMaterno']
    fechaNacimiento = form['fechaNacimiento']
    email = form['email']
    
    clave = generarClave(nombres, apellidoPaterno)
    print(clave)
    clave = codificar(clave)
    with Session() as session:
        usuario = Usuario(email, clave, 'Docente')
        session.add(usuario)
        session.commit()
        docente = Docente(nombres, apellidoPaterno, apellidoMaterno, fechaNacimiento, usuario.id)
        session.add(docente)
        session.commit()


def crearAdministrador(form):
    nombres = form['nombres']
    apellidoPaterno = form['apellidoPaterno']
    apellidoMaterno = form['apellidoMaterno']
    email = form['email']
    
    clave = generarClave(nombres, apellidoPaterno)
    print(clave)
    clave = codificar(clave)
    usuario = Usuario(email, clave, 'Administrador')
    session.add(usuario)
    session.commit()
    admin = Administrador(nombres, apellidoPaterno, apellidoMaterno, usuario.id)
    session.add(admin)
    session.commit()
    
def crearCurso(form):
    with Session() as session:
        nombre = form["nombre"]
        ciclo = form["ciclo"]
        duracion = form["duracion"]
        curso = Curso(duracion, ciclo, nombre)
        session.add(curso)
        session.commit()
    
def crearGrupo(form):
    with Session() as session:
        nombre = form["nombre"]
        codigo = form["codigo"]
        fechaInicio = form["fechaInicio"]
        fechaFinalizacion = form["fechaFinalizacion"]
        horaInicio = form["horaInicio"]
        horaFinalizacion = form["horaFinalizacion"]
        docente = form["docente"]
        curso = int(form["curso"])
        
        semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        dias = ""
        for i in semana:
            if form[i] == True:
                dias += f'{i}, '
        
        grupo = Grupo(fechaInicio, fechaFinalizacion, horaInicio, horaFinalizacion, docente, codigo, curso, dias, nombre)
        session.add(grupo)
        session.commit()
    
    
def obtenerRol(usuario:object):
    if usuario.rol == "Administrador":
        return session.query(Administrador).filter(Administrador.usuario).first()
    else:
        return session.query(Docente).filter(Docente.usuario).first()
    
    
def renderizarTemplate(plantilla):
    rol = session.get(Usuario, llaveAcceso())
    return render_template(plantilla, rol = rol, usuario = obtenerRol(rol))

def renderizarLista(plantilla:str, lista:list):
    rol = session.get(Usuario, llaveAcceso())
    return render_template(plantilla, rol = rol, usuario = obtenerRol(rol), lista = lista)

def renderizarJson(plantilla:str, json:dict):
    rol = session.get(Usuario, llaveAcceso())
    return render_template(plantilla, rol = rol, usuario = obtenerRol(rol), json = json)

def renderizarEdit(plantilla, objeto):
    rol = session.get(Usuario, llaveAcceso())
    return render_template(plantilla, rol = rol, usuario = obtenerRol(rol), registro = objeto)