from flask import session as nube
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
    
    
def obtenerRol(usuario:object):
    if usuario.rol == "Administrador":
        return session.query(Administrador).filter(Administrador.usuario).first()
    else:
        return session.query(Docente).filter(Docente.usuario).first()