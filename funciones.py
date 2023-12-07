from flask import session as nube
import hashlib
import base64

def validarSesion():
    if "llave_ingreso" in nube:
        return True
    return False

def codificar(texto):
    huella_digital = hashlib.sha256(texto.encode()).digest()
    texto_codificado = base64.b64encode(huella_digital)
    return texto_codificado.decode()


def decodificar(texto_codificado):
    texto_codificado = base64.b64decode(texto_codificado.encode())
    huella_digital = texto_codificado[:32]
    texto_descifrado = texto_codificado[32:].decode()
    return texto_descifrado

def validarClave(clave_codificada, clave_decodificada):
    return decodificar(clave_codificada) == clave_codificada


def verificar_caracteres_especiales(texto):
    texto = str(texto)
    for caracter in texto:
        if not caracter.isalnum():
            return False
    return True


def llaveAcceso():
    return nube["llaveAcceso"]
