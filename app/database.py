from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

# 1. Configuración de la base de datos
# ❌ ERROR QUE COMETÍA: Usar importaciones relativas (from .models import User)
#    Esto causaba circular imports porque los modelos también importaban entre sí
# ✅ SOLUCIÓN: Usar importaciones absolutas (from app.models) + TYPE_CHECKING
#    Las importaciones de modelos se hacen en lifespan() después de crear el engine
sqlite_name = "taskflow.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

# echo=True nos sirve para ver en la terminal cómo se crean las tablas (luego lo puedes quitar)
engine = create_engine(sqlite_url, echo=True)

# 🔥 EL TRUCO MAESTRO: TYPE_CHECKING + importaciones en lifespan()
# En lugar de importar los modelos aquí (lo que causaba circular imports),
# los importamos dentro de lifespan() después de configurar el engine.
# Esto permite que SQLModel.metadata.create_all(engine) reconozca los modelos
# sin crear problemas de importación circular.


# 2. Función para crear las tablas (que usas en el lifespan)
def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


# 3. Función para obtener la sesión de la base de datos
def get_session():
    with Session(engine) as session:
        yield session


# 4. Dependencia lista para usar en tus routers
Sessiondep = Annotated[Session, Depends(get_session)]
