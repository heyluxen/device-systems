**Aprendiz:** Valentina Correa Hoyos

**Ficha:** 3144585
# Device Systems API – FastAPI

# GA1-220501096-01-AA1-EV07 – Fundamentos de FastAPI: API REST para Gestión de Usuarios

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


## Tabla de endpoints

| Método | Ruta | Descripción | Códigos de estado |
|--------|------|-------------|-------------------|
| GET | `/api/v1/users` | Listar todos los usuarios (con filtros opcionales `?role`, `?is_active`) | 200 OK |
| GET | `/api/v1/users/{user_id}` | Obtener un usuario por su ID | 200 OK, 404 Not Found |
| POST | `/api/v1/users` | Crear un nuevo usuario | 201 Created, 400 Bad Request (email duplicado), 422 Unprocessable Entity |

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

# GA1-220501096-01-AA1-EV08 – FastAPI Intermedio: Evolución de device_systems con CRUD Completo, Manejo de Errores, Swagger/OpenAPI y Dependency Injection

# Introducción

En esta actividad evolucioné la API device_systems que había construido en la actividad anterior. Partí del proyecto base que ya tenía endpoints GET y POST, y lo convertí en una API REST completa con operaciones de actualización y eliminación.

Ahora el recurso users permite:

- Crear usuarios (POST).

- Listar y consultar por ID (GET).

- Actualizar completamente un usuario (PUT).

- Actualizar parcialmente (PATCH), por ejemplo, cambiar solo el rol o el email.

- Eliminar usuarios (DELETE).

Además, organicé el código separando responsabilidades en carpetas: routes, schemas, services, dependencies y data. Esto hizo el proyecto más limpio y fácil de mantener.

Implementé inyección de dependencias con Depends() para reutilizar la validación de existencia de usuarios. También mejoré el manejo de errores usando HTTPException con códigos HTTP adecuados (200, 201, 204, 400, 404, 422).

## Estructura del proyecto

![](images/estructura.png)

# Manejo de errores con HTTPException
- Se utilizaron códigos de estado HTTP apropiados y mensajes claros:

- 404 Not Found – cuando el recurso no existe.

- 400 Bad Request – email duplicado, PATCH sin campos, datos incorrectos.

- 422 Unprocessable Entity – errores de validación de Pydantic (nombre corto, email mal formado, rol no permitido).

- 201 Created – éxito al crear.

- 204 No Content – éxito al eliminar.

- 200 OK – éxito en consultas y actualizaciones.
--- 
# Dependency Injection

Se implementó una dependencia reutilizable en dependencies/user_dependencies.py para evitar duplicar la lógica de búsqueda de usuario y manejo de errores 404.

```python
# app/dependencies/user_dependencies.py
from fastapi import Depends, HTTPException, status
from app.services.user_service import get_user_by_id

def get_user_or_404(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user
```
Esta dependencia se inyecta en las rutas que necesitan un usuario existente:

```python
# app/routes/user_routes.py
from app.dependencies.user_dependencies import get_user_or_404

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user: dict = Depends(get_user_or_404)):
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_complete_user(user_id: int, user_data: UserCreate, user_exist: dict = Depends(get_user_or_404)):
    return update_user_complete(user_id, user_data)
```
Ventajas: centraliza la validación de existencia, reduce código repetido y mejora la mantenibilidad.


---

# Evidencias de pruebas

## Swagger UI – Documentación interactiva

![](images/documentacion2.png)
---

## Pruebas con PUT

![](images/captura12PUT.png)

Se realizó una petición PUT a http://localhost:8000/api/v1/users/1 enviando todos los campos del usuario (name, email, role, is_active). El usuario con ID 1 existía previamente, por lo que la API lo actualizó correctamente.

![](images/captura13PUT.png)

Se envió una petición PUT a http://localhost:8000/api/v1/users/1 con los campos actualizados: role cambió a "support" y is_active a false. La API reemplazó completamente los datos del usuario existente y devolvió el objeto actualizado.

Código HTTP: 200 OK


![](images/captura14PUT.png)

Se realizó una petición PUT a http://localhost:8000/api/v1/users/1 enviando todos los campos del usuario con nuevos valores: name = "Sofia Ortiz", email = "Sofia.O@example.com", role = "admin", is_active = true. El usuario existente fue reemplazado completamente y la API respondió con el objeto actualizado.

Código HTTP: 200 OK

![](images/captura15PUT.png)

Se intentó actualizar un usuario con ID 999 que no existe en la base de datos. La API validó el ID y respondió con un error indicando que el recurso no fue encontrado.

Código HTTP: 404 Not Found

## Pruebas con PATCH

![](images/captura16PATCH.png)

Se envió una petición PATCH a http://localhost:8000/api/v1/users/1 con el cuerpo {"role": "support"}, actualizando únicamente el campo role del usuario. Los demás campos (nombre, email, estado activo) permanecieron sin cambios. La API aplicó la actualización parcial y devolvió el objeto completo del usuario modificado.

Código HTTP: 200 OK

![](images/captura17PATCH.png)

Se realizó una petición PATCH a http://localhost:8000/api/v1/users/1 con el cuerpo {"email": "sofia.nuevoemail@example.com"}, actualizando únicamente el campo email del usuario. La API aplicó la actualización parcial y devolvió el objeto completo del usuario modificado, conservando el resto de campos sin cambios.

Código HTTP: 200 OK

![](images/captura18PATCH.png)

Se intentó realizar una actualización parcial enviando una petición PATCH a http://localhost:8000/api/v1/users/1 con un cuerpo JSON vacío ({}), es decir, sin ningún campo a modificar. La API detectó que no se proporcionó ningún dato válido para actualizar y rechazó la operación.

Código HTTP: 400 Bad Request

![](images/captura18,5PATCH.png)

Se intentó actualizar parcialmente un usuario con ID 999, el cual no existe en la base de datos. La API validó el ID y respondió con un error indicando que el recurso no fue encontrado, sin modificar ningún dato.

Código HTTP: 404 Not Found

## Pruebas con DELETE

![](images/captura19DELETE.png)

Se envió una petición DELETE a http://localhost:8000/api/v1/users/1 para eliminar al usuario con ID=1, el cual existía en la base de datos. La API procesó la eliminación correctamente y, al no retornar contenido en el cuerpo de la respuesta, utilizó el código de estado 204 No Content, indicando que la operación fue exitosa pero sin datos adicionales.

Código HTTP: 204 No Content

![](images/captura20DELETE.png)

Se envió una petición DELETE a http://localhost:8000/api/v1/users/1 intentando eliminar un usuario con ID=1 que ya había sido eliminado previamente o no existía en la base de datos. La API validó el ID y respondió con un error indicando que el recurso no fue encontrado.

Código HTTP: 404 Not Found

---
##  Tabla de endpoints (CRUD completo)

| Método | Ruta | Descripción | Códigos de estado |
|--------|------|-------------|-------------------|
| GET | `/api/v1/users` | Listar todos los usuarios (con filtros opcionales `?role`, `?is_active`) | 200 OK |
| GET | `/api/v1/users/{user_id}` | Obtener un usuario por su ID | 200 OK, 404 Not Found |
| POST | `/api/v1/users` | Crear un nuevo usuario | 201 Created, 400 Bad Request (email duplicado), 422 Unprocessable Entity |
| PUT | `/api/v1/users/{user_id}` | Actualizar completamente un usuario (todos los campos) | 200 OK, 404 Not Found, 400 Bad Request |
| PATCH | `/api/v1/users/{user_id}` | Actualizar parcialmente un usuario (solo campos enviados) | 200 OK, 404 Not Found, 400 Bad Request (body vacío) |
| DELETE | `/api/v1/users/{user_id}` | Eliminar un usuario | 204 No Content, 404 Not Found |

---
# GA1-220501096-01-AA1-EV09 – FastAPI con SQLAlchemy: Persistencia de Datos y CRUD sobre Base de Datos en device_systems

**Link video de YouTube:** https://youtu.be/OV3HhpEqdlk

En esta actividad evolucioné la API device_systems para que los usuarios ya no se guarden en la memoria del servidor (como en la actividad 8), sino en una base de datos real SQLite usando SQLAlchemy. Ahora, si apago y vuelvo a prender el servidor, los usuarios siguen ahí. También aprendí a separar los modelos de base de datos (SQLAlchemy) de los esquemas de validación (Pydantic), y a usar la inyección de dependencias con Depends(get_db) para manejar las sesiones de forma limpia. Al final, la API quedó más robusta, con persistencia real y preparada para crecer.

## Estructura del proyecto

![](images/estructura9.png)

## Base de datos generada

La API usa SQLite como motor de base de datos. Al ejecutar el servidor por primera vez, se crea automáticamente el archivo device_systems.db en la raíz del proyecto.

![](images/basededatos.png)

## Documentación Automática Swagger UI

![](images/documentacion9.png)


# Configuración de base de datos con SQLAlchemy
Archivo app/database/connection.py – Configura el motor y la sesión:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./device_systems.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)
```

Modelo User (app/models/user_model.py):

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    role = Column(String(20), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```
Inyección de dependencia (app/dependencies/database_dependency.py):

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
Cada endpoint recibe la sesión mediante Depends(get_db).
```

---
# Tabla de endpoints (CRUD completo)

| Método | Ruta | Descripción | Códigos de estado |
|--------|------|-------------|-------------------|
| GET | `/api/v1/users` | Listar todos (con filtros opcionales `?role`, `?is_active`) | 200 OK |
| GET | `/api/v1/users/{id}` | Obtener usuario por ID | 200 OK, 404 Not Found |
| POST | `/api/v1/users` | Crear usuario | 201 Created, 400 Bad Request (email duplicado), 422 Unprocessable Entity |
| PUT | `/api/v1/users/{id}` | Actualizar completamente | 200 OK, 404 Not Found, 400 Bad Request |
| PATCH | `/api/v1/users/{id}` | Actualizar parcialmente | 200 OK, 404 Not Found, 400 Bad Request (body vacío) |
| DELETE | `/api/v1/users/{id}` | Eliminar usuario | 204 No Content, 404 Not Found |

---

# Evidencias de pruebas por endpoint

## Pruebas exitosas

### POST – Crear usuario válido (201)
![](images/captura21.png)

### GET – Listar todos los usuarios (200)
![](images/captura23.png)

### GET – Usuario por ID existente (200)
![](images/captura24.png)

### PUT – Actualizar completo (200)
![](images/captura28.png)

### PATCH – Actualizar parcial (cambiar rol) (200)
![](images/captura29.png)

### DELETE – Eliminar usuario existente (204)
![](images/captura30.png)

### GET – Filtrar por rol (?role=admin) (200)
![](images/captura26.png)

### GET – Filtrar por activos (?is_active=true) (200)
![](images/captura27.png)


## Manejo de errores

### POST – Email duplicado	400 Bad Request
![](images/captura22ERROR.png)

### POST – Nombre muy corto (validación)	422 Unprocessable Entity
![](images/captura32ERROR.png)

### POST – Rol no permitido	422 Unprocessable Entity
![](images/captura33ERROR.png)

### GET – ID inexistente	404 Not Found
![](images/captura25ERROR.png)

### PATCH – Usuario no encontrado	404 Not Found
![](images/captura34ERROR.png)



### DELETE – Usuario inexistente	404 Not Found
![](images/captura35ERROR.png)

### GET – Validar que ya no existe (después de DELETE)	404 Not Found
![](images/captura31ERROR.png)


## Manejo de errores y códigos de estado

La API utiliza códigos HTTP estándar para comunicar el resultado de cada operación:

| Código | Significado | Cuándo ocurre |
|--------|-------------|----------------|
| 200 OK | Éxito | GET, PUT, PATCH exitosos |
| 201 Created | Recurso creado | POST /users válido |
| 204 No Content | Eliminación exitosa | DELETE /users/{id} (sin cuerpo) |
| 400 Bad Request | Error del cliente | Email duplicado, PATCH sin campos |
| 404 Not Found | Recurso no existe | GET/PUT/PATCH/DELETE con ID inexistente |
| 422 Unprocessable Entity | Validación fallida | Nombre corto, rol inválido, email mal formado |

---
## Dependency Injection con SQLAlchemy
Se implementó una dependencia reutilizable para la sesión de base de datos:

```python
# app/dependencies/database_dependency.py
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
Esta dependencia se inyecta en los endpoints usando Depends(get_db), garantizando que cada petición HTTP tenga su propia sesión y que se cierre automáticamente al finalizar.

Ejemplo en ruta:

```python
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_or_404(db, user_id)
```
---
# Reflexión final sobre la evolución del proyecto

Al inicio, device_systems guardaba los usuarios en una simple lista en memoria. Servía para aprender, pero tenía una gran limitación: al reiniciar el servidor, todos los datos desaparecían. No era una API útil en el mundo real.

La evolución más importante fue incorporar persistencia real con SQLAlchemy y SQLite. Ahora los usuarios se almacenan en una base de datos y sobreviven a los reinicios. Esto me hizo entender por qué las aplicaciones profesionales necesitan una base de datos.

También aprendí a separar responsabilidades: los modelos SQLAlchemy definen cómo se guardan los datos (tipos, restricciones como nullable y unique), mientras que los esquemas Pydantic definen cómo se validan y se muestran en la API. Esta separación mantiene el código limpio y seguro.

Otro avance fue usar inyección de dependencias con Depends(get_db). Cada petición HTTP recibe su propia sesión de base de datos y se cierra automáticamente. Esto evita errores de conexión y hace el código más reutilizable.

El manejo de errores también mejoró: ahora la API responde con códigos HTTP claros (200, 201, 204, 400, 404, 422) y mensajes descriptivos. El cliente siempre sabe qué pasó: si el email está duplicado, si el ID no existe o si los datos no son válidos.
