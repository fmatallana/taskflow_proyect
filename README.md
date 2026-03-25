# TaskFlow 📋

TaskFlow es una API REST construida con **FastAPI** y **SQLModel** para gestionar proyectos y tareas. Permite crear usuarios, proyectos y tareas asociadas, con relaciones bidireccionales entre modelos.

## ✨ Características

- 🔐 Gestión de usuarios
- 📁 Creación y consulta de proyectos
- ✅ Gestión de tareas con estados
- 🔗 Relaciones entre modelos (Usuario → Proyectos → Tareas)
- 💾 Base de datos SQLite integrada
- 📝 Documentación automática con Swagger UI

## 🚀 Requisitos previos

- Python 3.8+
- pip

## 📦 Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd taskflow
   ```

2. **Crear un entorno virtual (opcional pero recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

### URLs útiles:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

## 📚 Estructura del proyecto

```
taskflow/
├── app/
│   ├── main.py              # Punto de entrada, configuración de FastAPI
│   ├── database.py          # Configuración de BD, sesiones y dependencias
│   ├── models/              # Modelos SQLModel
│   │   ├── users.py         # Modelo User
│   │   ├── projects.py      # Modelo Project
│   │   └── tasks.py         # Modelo Task
│   └── routers/             # Rutas de la API
│       ├── users.py         # Endpoints de usuarios
│       ├── projects.py      # Endpoints de proyectos
│       └── tasks.py         # Endpoints de tareas
├── taskflow.sqlite3         # Base de datos (se crea automáticamente)
└── requirements.txt         # Dependencias del proyecto
```

## 🔌 Endpoints disponibles

### Usuarios `/users`
- `POST /users/` - Crear usuario
- `GET /users/{user_id}` - Obtener usuario por ID

### Proyectos `/projects`
- `GET /projects/` - Listar todos los proyectos
- `POST /projects/` - Crear proyecto
- `GET /projects/{project_id}` - Obtener proyecto por ID

### Tareas `/tasks`
- `GET /tasks/` - Listar todas las tareas
- `GET /tasks/project/{project_id}` - Obtener tareas de un proyecto
- `POST /tasks/` - Crear tarea
- `PUT /tasks/{task_id}` - Actualizar tarea
- `DELETE /tasks/{task_id}` - Eliminar tarea

## 📋 Ejemplo de uso (con curl)

### Crear un usuario
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "juan", "email": "juan@example.com"}'
```

### Crear un proyecto
```bash
curl -X POST "http://localhost:8000/projects/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Mi Proyecto", "description": "Descripción del proyecto", "user_id": 1}'
```

### Crear una tarea
```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Implementar API", "status": "pending", "project_id": 1}'
```

## 🏗️ Notas sobre la arquitectura

### Importaciones Absolutas
El proyecto utiliza **importaciones absolutas** (`from app.models import User`) en lugar de relativas para evitar problemas de circular imports que pueden ocurrir en aplicaciones complejas.

### TYPE_CHECKING
Se utiliza `TYPE_CHECKING` en los modelos para importar tipos solo durante el análisis estático, evitando circular imports en tiempo de ejecución mientras mantenemos type hints funcionales.

### NOQA: F401
En `main.py`, las importaciones de modelos usan `# noqa: F401` porque se importan indirectamente para ser registradas en SQLModel.metadata antes de crear las tablas, aunque no se usen directamente en el código.

## 🛠️ Tecnologías utilizadas

- **FastAPI** - Framework web moderno y rápido
- **SQLModel** - ORM que combina SQLAlchemy y Pydantic
- **SQLite** - Base de datos relacional ligera
- **Uvicorn** - Servidor ASGI

## 📝 Licencia

Este proyecto es de código libre.
