**Aprendiz:** Valentina Correa Hoyos

**Ficha:** 3144585

# GA1-220501096-01-AA1-EV07 – Fundamentos de FastAPI: API REST para Gestión de Usuarios

**Link video de Youtube:** https://youtu.be/fzrc7cCX3jo

## Introducción

En este trabajo hice una API REST llamada `device_systems` usando FastAPI. La API sirve para administrar usuarios: puedes crearlos, listarlos, buscarlos por ID, filtrarlos por rol o por si están activos o no.

Para guardar los usuarios usé una lista en memoria (como una base de datos falsa mientras hago las pruebas). Los datos se validan automáticamente con Pydantic: el nombre debe tener al menos 3 letras, el email tiene que tener un formato válido, el rol solo puede ser `admin`, `support` o `user`, y el estado `is_active` es verdadero o falso.

También agregué cabeceras personalizadas en las respuestas (`X-App-Name` y `X-API-Version`) y usé modelos de respuesta para no mostrar información que no hace falta.

Probé todos los endpoints con Insomnia y también revisé la documentación automática que genera FastAPI en `http://localhost:8000/docs`. En las siguientes capturas se ven las pruebas exitosas y los errores de validación. Al final dejo una pequeña reflexión sobre lo que me pareció trabajar con FastAPI.

---

# Instalación y ejecución


## Crear entorno virtual
python -m venv venv
## Activar (Windows)
venv\Scripts\activate
## Instalar dependencias
pip install fastapi uvicorn email-validator
## Correr el servidor
uvicorn app.main:app --reload
La API estará en http://localhost:8000

Documentación Swagger UI: http://localhost:8000/docs

# Evidencias de pruebas
## 1. Swagger UI – Documentación interactiva
![](images/documentacion.png)

Swagger UI se genera automáticamente. Aquí se ven todos los endpoints disponibles y se pueden probar.

## 2. POST /users – Usuario creado exitosamente (201)

![](images/captura1.png)

Se envía un usuario con nombre "Diana Hoyos", email válido y rol "admin". FastAPI responde con código 201 y devuelve el usuario creado con un ID asignado.

## 3. POST /users – Error por nombre muy corto (422)
![](images/captura3.png)

Se intenta crear un usuario con nombre "An" (menos de 3 caracteres). La validación falla y FastAPI responde con error 422 indicando que el nombre debe tener al menos 3 caracteres.

## 4. POST /users – Error por email duplicado (400)
![](images/captura2.png)

Se envía un email que ya está registrado. La API detecta la duplicidad y responde con código 400 y un mensaje claro.

## 5. POST /users – Error por rol inválido (422)
![](images/captura4.png)

Se envía el rol "superuser" que no está permitido. Solo se aceptan "admin", "support" o "user". El error 422 especifica el problema.

## 6. POST /users – Error por email mal formado (422)
![](images/captura5.png)

Se envía un email sin "@". La validación de Pydantic lo rechaza y devuelve un error explicativo.

## 7. GET /users – Listar todos los usuarios
![](images/captura6.png)

Se obtienen todos los usuarios registrados hasta el momento. La respuesta es un arreglo JSON con cada usuario.

## 8. GET /users?role=admin – Filtrar por rol
![](images/captura7.png)

Se consulta la lista de usuarios filtrando por rol "admin". Solo aparecen los usuarios que tienen ese rol.

## 9. GET /users?is_active=false – Filtrar inactivos
![](images/captura8.png)

Se filtran los usuarios que están inactivos. En este caso no hay ninguno, por lo que la respuesta es un arreglo vacío.

## 10. GET /users/3 – Usuario existente
![](images/captura9.png)

Se consulta un usuario por su ID (3). Como existe, la API responde con código 200 y sus datos.

## 11. GET /users/100 – Usuario no encontrado (404)
![](images/captura10.png)

Se pide un ID que no corresponde a ningún usuario. La API responde con 404 y el mensaje "Usuario no encontrado".

## 12. Cabeceras personalizadas
![](images/captura11.png)

En todas las respuestas se incluyen las cabeceras X-App-Name: device_systems y X-API-Version: 1.0. En la captura se ven dentro de Insomnia.

# Reflexión sobre FastAPI
FastAPI me pareció muy fácil de usar. Con solo escribir los modelos de Pydantic ya obtienes validación y documentación automática. No tuve que escribir mucho código repetitivo. Los errores de validación (422) son claros y ayudan a saber qué está mal.

La parte de cabeceras personalizadas y parámetros de consulta (?role=admin) es muy directa. También me gustó que puedas ocultar datos sensibles con response_model.

El único problema fue acordarme de instalar email-validator y de poner las rutas fijas antes de las dinámicas para que no se confundan.

En general, FastAPI es ideal para hacer APIs rápidas, limpias y con buen rendimiento. Lo recomiendo para proyectos pequeños y grandes.
