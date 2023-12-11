from database import *
import pandas as pd
from tkinter import filedialog, messagebox
import datetime
from datetime import date
class Cargador:
    
    def __init__(self, archivo):
        
        
        hojaEstudiantes = "ASISTENCIA".upper()
        
        
        registrosDeEstudiantes = pd.read_excel(
            archivo, sheet_name=hojaEstudiantes)
        
        
        
        for index, fila in registrosDeEstudiantes.iterrows():
            
            estudiantes_repetidos = []
            print(fila['CODIGO'], datetime.datetime.now().date(), fila['NOMBRE'], fila['DiaDePago'], fila['GRUPO'])
            estudiante = Estudiante(fila['CODIGO'], datetime.datetime.now().date(), fila['NOMBRE'], date.today().replace(day=fila['DiaDePago']), fila['GRUPO'])
            
            try:
                session.add(estudiante)
            except:
                estudiantes_repetidos.append(estudiante)
        
        session.commit()
