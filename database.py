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
    __tablename__ = 'usarios'
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
        self.fecha_nacimiento = fecha_nacimiento
        self.usuario = usuario


class Administrador(Base):
    __tablename__ = 'administradores'
    id = Column(Integer, primary_key=True)
    nombres = Column(String(225), nullable=False)
    apellido_paterno = Column(String(225), nullable=False)
    apellido_materno = Column(String(225), nullable=False)
    usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    def __init__(self, nombres, apellido_paterno, apellido_materno, fecha_nacimiento, usuario):
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.usuario = usuario