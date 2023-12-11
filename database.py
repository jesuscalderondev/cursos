from sqlalchemy import func, UniqueConstraint, create_engine, Column, Integer, String, DECIMAL, DateTime, Time, Uuid
from sqlalchemy import Float, Date, Numeric, ForeignKey, or_, Boolean, and_
import sqlalchemy.dialects.sqlite
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from datetime import datetime, date, time, timedelta
from dateutil.parser import parse
import uuid

engine = create_engine('sqlite:///database.db')

# Crea una sesión de la base de datos utilizando el objeto sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# Define la estructura de la tabla utilizando la clase declarative_base
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    clave = Column(String(12), nullable=False)
    rol = Column(String(15), nullable=False)
    estado = Column(Boolean, nullable=True)
    
    def __init__(self, email, clave, rol):
        self.email = email
        self.clave = clave
        self.rol = rol
        self.estado = 1
    
        
class Docente(Base):
    __tablename__ = 'docentes'
    id = Column(Integer, primary_key=True)
    nombres = Column(String(225), nullable=False)
    apellido_paterno = Column(String(225), nullable=False)
    apellido_materno = Column(String(225), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    def __init__(self, nombres, apellido_paterno, apellido_materno, fecha_nacimiento, usuario):
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
        self.usuario = usuario

class Administrador(Base):
    __tablename__ = 'administradores'
    id = Column(Integer, primary_key=True)
    nombres = Column(String(225), nullable=False)
    apellido_paterno = Column(String(225), nullable=False)
    apellido_materno = Column(String(225), nullable=False)
    usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    def __init__(self, nombres, apellido_paterno, apellido_materno, usuario):
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.usuario = usuario
        
class Curso(Base):
    __tablename__ = 'cursos'
    codigo = Column(Integer, primary_key=True)
    duracion = Column(Integer, nullable=False)
    ciclo = Column(String(122), nullable=False)
    nombre = Column(String(122), nullable=False)
    
    def __init__(self, duracion, ciclo, nombre):
        self.nombre = nombre
        self.ciclo = ciclo
        self.duracion = duracion
        
class Grupo(Base):
    __tablename__ = 'grupos'
    codigo = Column(String, primary_key=True, autoincrement=False)
    fecha_inicial = Column(Date, nullable=False)
    fecha_final = Column(Date, nullable=False)
    hora_inicial = Column(Time, nullable = False)
    hora_final = Column(Time, nullable = False)
    dias_de_clases = Column(String(255), nullable=False)
    docente = Column(Integer, ForeignKey("docentes.id"), nullable=True)
    curso = Column(Integer, ForeignKey("cursos.codigo"), nullable=False)
    nombre = Column(String(255), nullable = False)
    
    def __init__(self, fecha_inicial, fecha_final, hora_inicial, hora_final, docente, codigo, curso, dias, nombre):
        self.codigo = codigo
        self.hora_inicial = datetime.strptime(hora_inicial, "%H:%M").time()
        self.hora_final = datetime.strptime(hora_final, "%H:%M").time()
        self.fecha_inicial = datetime.strptime(fecha_inicial, "%Y-%m-%d").date()
        self.fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d").date()
        self.docente = docente
        self.curso = curso
        self.dias_de_clases = dias
        self.nombre = nombre
        
        
class Estudiante(Base):
    __tablename__ = 'estudiantes'
    codigo = Column(Integer, primary_key=True, autoincrement=False)
    fecha_creacion = Column(Date, nullable=False)
    nombre = Column(String(225), nullable=False)
    dia_de_pago = Column(Date, nullable = True)
    grupo = Column(String, ForeignKey('grupos.codigo'), nullable=False)
    
    
    def __init__(self, codigo, fechaDeCreacion, nombre, diaDePago, grupo):
        self.codigo = codigo
        self.nombre = nombre
        self.dia_de_pago = diaDePago
        self.fecha_creacion = fechaDeCreacion
        self.grupo = grupo
        
class AsistenciaDocente(Base):
    __tablename__ = 'asistencia_de_docentes'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable = False)
    docente = Column(Integer, ForeignKey('docentes.id'), nullable=False)
    grupo = Column(String, ForeignKey('grupos.codigo'), nullable = False)
    
    def __init__(self, docente, fecha, grupo):
        self.fecha = fecha
        self.docente = docente
        self.grupo = grupo
        
        
class AsistenciaEstudiante(Base):
    __tablename__ = 'asistencia_de_estudiantes'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable = False)
    estudiante = Column(Integer, ForeignKey('estudiantes.codigo'), nullable=False)
    grupo = Column(String, ForeignKey('grupos.codigo'), nullable = False)
    asiste = Column(Boolean, nullable=False)
    
    def __init__(self, estudiante, grupo, asiste):
        self.fecha = datetime.now().date()
        self.estudiante = estudiante
        self.grupo = grupo
        self.asiste = asiste