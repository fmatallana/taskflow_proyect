from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

# 🔵 IMPORTACIONES ABSOLUTAS (app.xxx)
# Cambio de importaciones relativas a absolutas para evitar problemas de circular imports
# que ocurrían cuando usábamos "from .database import" en archivos que se importaban entre sí
from app.database import engine
from app.routers import projects, tasks, users

"""lifespan espera una función especial (un generador asíncrono) y no directamente la función que crea las tablas
En las versiones más modernas de FastAPI, se hace así para que la base de datos se prepare justo antes de que el servidor acepte peticiones"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 NOQA: F401 ("IMPORTADO PERO NO UTILIZADO")
    # Estos modelos NO se usan directamente aquí, pero los importamos para registrarlos
    # en SQLModel.metadata ANTES de crear las tablas. Sin estas importaciones, SQLModel
    # no sabría que existen esos modelos y no crearía sus tablas en la BD.
    # El comentario "# noqa: F401" silencia la advertencia del linter
    from app.models.projects import Project  # noqa: F401
    from app.models.tasks import Task  # noqa: F401
    from app.models.users import User  # noqa: F401

    # El código aquí se ejecuta al INICIAR la app
    SQLModel.metadata.create_all(engine)
    yield
    # El código aquí se ejecuta al APAGAR la app (si necesitas cerrar conexiones)


app = FastAPI(lifespan=lifespan)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(users.router)
