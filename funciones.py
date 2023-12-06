from flask import session as nube

def validar_sesion():
    if "llave_ingreso" in nube:
        return True
    return False