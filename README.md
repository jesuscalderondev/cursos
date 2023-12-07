# cursos




### Respuesta a la dirección "/api/filtrar_docente"

Al hacer la petición al serviodor se obtienen dos posibles estados, si no existe credencial dentro del servidor se retorna un json de la siguiente manera:

```js
json = {
    'respuesta' : 'Acceso denegado'
}
```
Por el contrario si se tiene la credencial se obtiene un json de este estilo:

```js

json = {
    'respuesta' : 'Acceso concedido',

    'docentes' : {
        '1' : {
            'nombres' : 'Juan Andrés',
            'paterno' : 'Carrasco',
            'materno' : 'Fuentes',
            'email' : 'docenteemail@gmail.com',
            'id' : 1
        },
        '7' : {
            'nombres' : 'Carlos Camilo',
            'paterno' : 'Torres',
            'materno' : 'Dominguez',
            'email' : 'carlostorres@gmail.com',
            'id' : 7
        },
    }
}

```

### Respuesta a la dirección 

La función comienza verificando si el usuario ya está autenticado. Si no lo está, procede a obtener las credenciales del usuario desde la solicitud. Luego, verifica que las credenciales no contengan caracteres especiales. Si no contienen caracteres especiales, la función procede a obtener el usuario de la base de datos. Si el usuario existe y la clave es correcta, la función actualiza la nube con la llave de ingreso del usuario y establece la operación como "Exitosa". En caso contrario, la función establece la operación como "Fallida" y el mensaje como "Usuario o clave incorrect@". Finalmente, la función devuelve la respuesta.


Vista de json

```js

json = {
    'respuesta' : 'Exitosa',
    'mensaje' : 'Usuario o clave incorrect@'
}
```