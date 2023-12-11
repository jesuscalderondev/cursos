from database import *
import pandas as pd
from tkinter import filedialog, messagebox
from datetime import *
from datetime import date, datetime
class Cargador:
    
    def __init__(self, archivo):
        
        
        cursos = [
            "Inglés",
            "Mates",
            "Python",
            "Fundamentos",
            "Algoritmos",
            "POO",
            "Programación funcional",
            "POO avanzada",
            "Desarrollo web",
            "Desarrollo web",
            "Desarrollo móvil",
            "Machine Learning",
            "Deep Learning",
            "Ciencia de datos",
            "IA",
            "Robótica",
        ]

        grupos_creados = []
        cursos_creados = 0
        hojaEstudiantes = "ASISTENCIA".upper()
        
        
        registrosDeEstudiantes = pd.read_excel(
            archivo, sheet_name=hojaEstudiantes)
        
        
        
        for index, fila in registrosDeEstudiantes.iterrows():
            
            estudiantes_repetidos = []
            print(fila['CODIGO'], datetime.now().date(), fila['NOMBRE'], fila['DiaDePago'], fila['GRUPO'])
            estudiante = Estudiante(fila['CODIGO'], datetime.now().date(), fila['NOMBRE'], date.today().replace(day=fila['DiaDePago']), fila['GRUPO'])
            
            if cursos_creados == 0 or len(grupos_creados)%16 == 0:
                curso = Curso(128, "2024-II", cursos[cursos_creados])
                cursos_creados += 1
                session.add(curso)
            
            if fila['GRUPO'] not in grupos_creados:
                grupo = Grupo("2024-01-01", "2024-06-01", "08:00", "10:00", 1, fila['GRUPO'], cursos_creados, "Lunes, Martes, Viernes, ", f"Grupo {index}")
                grupos_creados.append(fila['GRUPO'])
                session.add(grupo)
                print(grupo.curso)
            try:
                session.add(estudiante)
            except:
                estudiantes_repetidos.append(estudiante)
        
        session.commit()
