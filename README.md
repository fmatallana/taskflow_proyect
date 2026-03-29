# TaskFlow - Task Management API

![Status](https://img.shields.io/badge/Status-FINAL%20RELEASE-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688?logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)

## 📋 Descripción

TaskFlow es una **API REST moderna y escalable** para la gestión integral de proyectos y tareas. Construida con **FastAPI** y **SQLModel**, proporciona un entorno robusto para la organización y seguimiento de proyectos, con autenticación segura basada en JWT y modelado de datos relacional.

### Características Principales

- 🔐 **Autenticación y Autorización** - Sistema de autenticación JWT con hashing bcrypt
- 👥 **Gestión de Usuarios** - Registro seguro y manejo de cuentas de usuario
- 📁 **Gestión de Proyectos** - Crear, actualizar y administrar proyectos
- ✅ **Gestión de Tareas** - Control completo del ciclo de vida de las tareas
- 🔗 **Relaciones Bidireccionales** - Arquitectura relacional limpia (Usuario → Proyectos → Tareas)
- 💾 **Base de Datos SQLite** - Persistencia de datos local integrada
- 📚 **Documentación Interactiva** - Swagger UI y ReDoc automáticos
- ✔️ **Type-Safety** - Validación robusta con Pydantic v2
- 🚀 **Async/Await** - Operaciones completamente asíncronas

## 🛠️ Stack Tecnológico

| Component | Technology |
|-----------|------------|
| **Framework** | FastAPI 0.135.2 |
| **Web Server** | Uvicorn 0.42.0 |
| **ORM** | SQLModel 0.0.37 / SQLAlchemy 2.0.48 |
| **Validation** | Pydantic 2.12.5 |
| **Authentication** | PyJWT 2.12.1 + bcrypt 3.2.2 |
| **Database** | SQLite3 |
| **Testing** | pytest 9.0.2 |

## ⚙️ Requisitos Previos

- **Python** 3.8 o superior
- **pip** (gestor de paquetes de Python)
- **Git** (para clonar el repositorio)

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/taskflow.git
cd taskflow
```

### 2. Crear entorno virtual (recomendado)

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🚀 Ejecución

### Modo desarrollo con auto-reload

```bash
uvicorn app.main:app --reload
```

### Modo producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Acceso a la API

Una vez iniciado el servidor, accede a:

| Recurso | URL |
|---------|-----|
| **API Base** | http://localhost:8000 |
| **Swagger UI** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **OpenAPI Schema** | http://localhost:8000/openapi.json |

## 📂 Estructura del Proyecto

```
taskflow/
├── app/
│   ├── main.py                 # Punto de entrada principal
│   ├── database.py             # Configuración de BD y sesiones
│   ├── security.py             # Lógica de autenticación JWT
│   ├── models/
│   │   ├── __init__.py
│   │   ├── users.py           # Modelo User y esquemas relacionados
│   │   ├── projects.py        # Modelo Project y esquemas
│   │   └── tasks.py           # Modelo Task y esquemas
│   └── routers/
│       ├── __init__.py
│       ├── users.py           # Endpoints: registro, login, usuario
│       ├── projects.py        # Endpoints: CRUD de proyectos
│       └── tasks.py           # Endpoints: CRUD de tareas
├── taskflow.sqlite3           # Base de datos (creada automáticamente)
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Este archivo
└── .gitignore                # Archivos ignorados en Git
```

## 🔌 Referencia de Endpoints

### Usuarios (`/users`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/users/` | Crear nuevo usuario |
| `POST` | `/users/login` | Autenticarse y obtener token JWT |
| `GET` | `/users/{user_id}` | Obtener información del usuario |

### Proyectos (`/projects`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/projects/` | Listar todos los proyectos |
| `POST` | `/projects/` | Crear nuevo proyecto |
| `GET` | `/projects/{project_id}` | Obtener detalles del proyecto |
| `PUT` | `/projects/{project_id}` | Actualizar proyecto |
| `DELETE` | `/projects/{project_id}` | Eliminar proyecto |

### Tareas (`/tasks`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/tasks/` | Listar todas las tareas |
| `GET` | `/tasks/project/{project_id}` | Obtener tareas de un proyecto |
| `POST` | `/tasks/` | Crear nueva tarea |
| `PUT` | `/tasks/{task_id}` | Actualizar tarea |
| `DELETE` | `/tasks/{task_id}` | Eliminar tarea |

## 🔐 Autenticación

TaskFlow implementa **autenticación JWT (JSON Web Tokens)** para asegurar los endpoints.

### Flujo de autenticación

1. **Registro de usuario**
   ```bash
   curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"username": "juan", "email": "juan@example.com", "password": "secure_password_123"}'
   ```

2. **Obtener token de acceso (login)**
   ```bash
   curl -X POST "http://localhost:8000/users/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "juan", "password": "secure_password_123"}'
   ```

   **Respuesta:**
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```

3. **Usar token en solicitudes autenticadas**
   ```bash
   curl -X GET "http://localhost:8000/projects/" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
   ```

**Características de seguridad:**
- Contraseñas hasheadas con bcrypt
- Tokens JWT con expiración (30 minutos por defecto)
- Validación de credenciales en cada request

## 📋 Ejemplos de Uso

### Crear un usuario

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan",
    "email": "juan@example.com",
    "password": "mi_contraseña_segura"
  }'
```

### Crear un proyecto

```bash
curl -X POST "http://localhost:8000/projects/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "Sistema de Inventario",
    "description": "Aplicación web para gestión de inventario",
    "user_id": 1
  }'
```

### Crear una tarea

```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Diseñar base de datos",
    "description": "Crear schema inicial",
    "project_id": 1,
    "status": "pending"
  }'
```

### Obtener tareas de un proyecto

```bash
curl -X GET "http://localhost:8000/tasks/project/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🏗️ Notas sobre la Arquitectura

### Importaciones Absolutas

El proyecto utiliza **importaciones absolutas** (`from app.models import User`) en lugar de importaciones relativas para evitar problemas de circular imports. Este patrón es especialmente importante en aplicaciones complejas con múltiples dependencias entre módulos.

### TYPE_CHECKING

En los modelos se utiliza `TYPE_CHECKING` para importar tipos solo durante el análisis estático del código, evitando circular imports en tiempo de ejecución mientras se mantienen los type hints completamente funcionales.

### NOQA: F401

En `main.py`, las importaciones de modelos usan el comentario `# noqa: F401` porque se importan indirectamente para ser registradas en `SQLModel.metadata` antes de crear las tablas en la base de datos, aunque no se usen directamente en el código.

## 📖 Desarrollo

### Ejecutar tests

```bash
pytest
```

### Instalar dependencias de desarrollo

```bash
pip install -r requirements.txt -e .
```

## 🤝 Contribuciones

Este proyecto marca el cierre de su ciclo de desarrollo. No se aceptan nuevas contribuciones.

## 📝 Licencia

MIT License - Ver detalles en LICENSE

## 📌 Versionado

**Versión Final:** 1.0.0 (Marzo 2026)

---

**Estado del Proyecto:** ✅ **COMPLETADO Y CERRADO**

*Última actualización: Marzo 29, 2026*
